import requests
from plot_ping import generate_plots
from read_json import json_to_graph
from id_fetcher import get_starlink_probe_ids
from fake_data import test_plots_with_fake_data
from ping_sites import ping_google

prefix = 'https://atlas.ripe.net/api/v2/'
msm_id = 52793844


# TELL THE SCRIPT WHAT TO RUN HERE
FETCH_IDS = False
PING_GOOGLE = False
TEST_GRAPHING = False
GENERATE_PLOT = True



def main():
    if FETCH_IDS or PING_GOOGLE or TEST_GRAPHING:
        starlink_probe_ids = get_starlink_probe_ids()
        num_starlink_probes = len(starlink_probe_ids)
        print("Found " + str(num_starlink_probes) + " Starlink probes with IDs:\n")
        print(starlink_probe_ids)
    if PING_GOOGLE:
        ping_google(starlink_probe_ids)
    if TEST_GRAPHING:
        test_plots_with_fake_data(num_starlink_probes)
    if GENERATE_PLOT:
        r = requests.get(prefix + 'measurements/'+ str(msm_id) + '/results')
        j = r.json()
        data = json_to_graph(j)
        generate_plots(data)
    

main()