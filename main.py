import requests
from plot_ping import generate_plots, geo_plot
from read_json import json_to_graph, json_to_time
from id_fetcher import get_starlink_probe_ids
from fake_data import test_plots_with_fake_data
from ping_sites import ping_google
from datetime import datetime, tzinfo, timedelta

prefix = 'https://atlas.ripe.net/api/v2/'

HOURS_IN_DAY = 24
MIN_IN_HOUR = 60

DAYS_OF_REQUESTS = 1

MIN_BETWEEN_REQUESTS = 15
S_BETWEEN_REQUESTS = MIN_BETWEEN_REQUESTS * 60
MS_BETWEEN_REQUESTS = S_BETWEEN_REQUESTS * 1000

TEST_GRAPHING = False
ID_LIST = [
    61537, 60929, 61113, 60510, 52955, 52918, 1004453, 1005627, 26834, 1004876,
    1002827, 1002750, 35681, 17979, 20544
]

na = [61537, 60929, 61113, 60510]
aus = [52955, 52918, 1004453]
carr = [1005627]
sa = [26834]
eu = [1004876, 1002827, 1002750, 35681, 17979, 20544]
colors = {
    'North America': 'coral',
    'Australia': 'cornflowerblue',
    'Caribbean': 'lightseagreen',
    'South America': 'mediumvioletred',
    'Europe': 'gold'
}

# Map each ID to a country
country_map = {
    i:
    'North America' if i in na else 'Australia' if i in aus else
    'Caribbean' if i in carr else 'South America' if i in sa else 'Europe'
    for i in ID_LIST
}

# Map each country to a color
color_map = {country: colors[color] for country, color in country_map.items()}

msm_id = 52793844

# TELL THE SCRIPT WHAT TO RUN HERE
FETCH_IDS = False
PING_GOOGLE = False
TEST_GRAPHING = False
GENERATE_PLOT = True
GENERATE_MAP = True


def get_coords(ids):
    """
		Helper function
		Given a list of probe ids, we return a dictionary that maps the ids to some 
		(latitute, longitude, countrycode) tuple
		Yes geoJSON flips them (long, lat). I think that's BS so I'm re-flipping them. 
		So it's the correct way.
		The only way.
		"""
    ids_to_str = str(ids)[1:-1]
    r = requests.get(prefix + 'probes?id__in=' + ids_to_str)
    j = r.json()

    position = {}

    # print("j is " + repr(j))
    for res in j['results']:
        key = res['id']
        cs = res["country_code"]
        geometry = res['geometry']['coordinates']
        loc = (geometry[1], geometry[0], cs)
        position[key] = loc
    return position


def main():
    if FETCH_IDS or PING_GOOGLE or TEST_GRAPHING or GENERATE_MAP:
        #starlink_probe_ids = get_starlink_probe_ids()
        starlink_probe_ids = ID_LIST
        coordinates = get_coords(starlink_probe_ids)

        #if you want to include the backup
        num_starlink_probes = len(starlink_probe_ids)
        print("Found " + str(num_starlink_probes) +
              " Starlink probes with IDs:\n")
        print(starlink_probe_ids)
    if PING_GOOGLE:
        ping_google(starlink_probe_ids)
    if TEST_GRAPHING:
        test_plots_with_fake_data(num_starlink_probes)
    if GENERATE_PLOT:
        r = requests.get(prefix + 'measurements/' + str(msm_id) + '/results')
        j = r.json()
        data = json_to_graph(j)
        generate_plots(data)
    if GENERATE_MAP:
        r = requests.get(prefix + 'measurements/' + str(msm_id) + '/results')
        j = r.json()
        data_time_sort = json_to_time(j)
        geo_plot(data_time_sort, coordinates)


main()