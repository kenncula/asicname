'''
ripe.atlas.cousteau library: 
This is a Python library provided by RIPE Atlas that provides a convenient 
interface for working with the RIPE Atlas API. You can use it to set up and 
execute ping measurements, and retrieve the results.

MeasurementRequest() method: 
This method allows you to create a new measurement request, which you can 
use to define the parameters of the ping measurement you want to perform. 
You can specify the target IP address or hostname, the number of packets 
to send, the interval between packets, and other parameters.

AtlasSource() method: 
This method allows you to specify the source of the ping measurement. 
You can specify a single RIPE Atlas probe, a set of probes, or a group of probes.

AtlasCreateRequest() method: 
This method allows you to create a new measurement request using the 
parameters you have specified.

AtlasResultsRequest() method: 
This method allows you to retrieve the results of a measurement request. 
You can use it to get the ping times for each packet, as well as other 
information such as the number of packets lost.'''
'''
from ripe.atlas.cousteau import AtlasSource, AtlasCreateRequest, AtlasResultsRequest

# Set up the measurement parameters
ping_count = 10
target_address = "example.com"

# Set up the source of the measurement
atlas_source = AtlasSource(type="probes", value="US")

# Create the measurement request
ping_request = AtlasCreateRequest(
    start_time=None,
    key=None,
    measurements=[{
        "type": "ping",
        "af": 4,
        "target": target_address,
        "description": "Ping measurement",
        "interval": 300,
        "packets": ping_count,
    }],
    sources=[atlas_source],
    is_oneoff=True
)

# Submit the measurement request and get the measurement ID
ping_response = ping_request.create()
measurement_id = ping_response["measurements"][0]

# Wait for the measurement to complete
while True:
    is_completed = AtlasResultsRequest(msm_id=measurement_id).create().is_success()
    if is_completed:
        break

# Get the results of the measurement
ping_results = AtlasResultsRequest(msm_id=measurement_id).create()
ping_times = [result["result"]["rtt"] for result in ping_results]

This is chatgpt Code: DO NOT TRUST
'''
import requests
from plot_ping import generate_plots, geo_plot
from datetime import datetime, tzinfo, timedelta
import random
from read_json import json_to_graph, json_to_time
import json

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


def get_starlink_probe_ids():
    params = dict()
    #params['tags'] = 'starlink'
    params['asn'] = 14593
    params['status_name'] = 'Connected'
    params['is_public'] = True

    r = requests.get(prefix + 'probes/', params=params)
    j = r.json()

    ids = []

    for res in j['results']:
        ids.append(res['id'])
    return ids


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


def update_json(msm, save_locally=True, save_path='measurements.json'):
    # 52793844
    r = requests.get(prefix + 'measurements/' + str(msm) + '/results')
    data = r.json()
    if save_locally:
        with open(save_path, 'w') as f:
            json.dump(data, f)
    return data


def generate_fake_time_data(start_time):
    times = []
    d = datetime.now()
    for j in range(
            start_time, start_time +
        (int)(HOURS_IN_DAY * MIN_IN_HOUR / MIN_BETWEEN_REQUESTS)):
        times.append(
            datetime(d.year, d.month, d.day) + timedelta(0, 0, 0, 0, (15 * j)))
    return times


def generate_fake_latency_data(start_time):
    data = []
    for j in range(
            start_time, start_time +
        (int)(HOURS_IN_DAY * MIN_IN_HOUR / MIN_BETWEEN_REQUESTS)):
        data.append(random.randint(0, 200))
    return data


def test_plots_with_fake_data(num_probes):
    data = []
    for i in range(num_probes):
        fake_time_data = generate_fake_time_data(0)
        fake_latency_data = generate_fake_latency_data(0)
        d = [(fake_time_data[i], fake_latency_data[i])
             for i in range(0, len(fake_time_data))]
        data.append(d)
    generate_plots(data)


def main():
    #starlink_probe_ids = get_starlink_probe_ids()
    starlink_probe_ids = ID_LIST
    coordinates = get_coords(starlink_probe_ids)
    num_starlink_probes = len(starlink_probe_ids)
    print("Starlink Probe IDs for " + str(num_starlink_probes) + " Probes:")
    print(starlink_probe_ids)
    if TEST_GRAPHING:
        test_plots_with_fake_data(num_starlink_probes)

    update_json(52793844)
    data = json_to_graph('measurements.json')
    data_time_sort = json_to_time('measurements.json')

    generate_plots(data, coordinates, color_map)
    geo_plot(data_time_sort, coordinates)


main()