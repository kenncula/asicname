import requests
from plot_ping import generate_plots
from read_json import json_to_graph
from id_fetcher import get_starlink_probe_ids
from fake_data import test_plots_with_fake_data

prefix = 'https://atlas.ripe.net/api/v2/'

msm_id = 52793844

FETCH_IDS = False
TEST_GRAPHING = False

def get_starlink_probe_ids():
    params = dict()
    params['tags'] = 'starlink'
    params['status_name'] = 'Connected'
    params['is_public'] = True

    r = requests.get(prefix + 'probes/', params=params)
    j = r.json()

    ids = []

    for res in j['results']:
        ids.append(res['id'])
    return ids

starlink_ids=get_starlink_ids()

from ripe.atlas.cousteau import Ping
from ripe.atlas.cousteau import AtlasSource

ping = Ping(
    af=4,
    target="google.com",
    description="Ping Test",
    #interval=900, #this sets the interval to ping every 15 minutes
    is_oneoff=True #this is for testing,
)
str_ids=str(starlink_ids)
table=str_ids.maketrans('','',' []')
trans_ids=str_ids.translate(table)

source = AtlasSource(
    type="probes",
    value=trans_ids,
    requested=len(starlink_ids)
)

from datetime import datetime
from ripe.atlas.cousteau import (
  AtlasSource,
  AtlasCreateRequest
)

ATLAS_API_KEY = "9b60b650-68bf-4c40-bbcc-a2b8d3e15779"

atlas_request = AtlasCreateRequest(
    key=ATLAS_API_KEY,
    measurements=[ping],
    sources=[source],
    is_oneoff=True
)

import re
(is_success, response) = atlas_request.create()
id=re.sub("[^0-9]", "", str(response))
print("msm_id:" + id)

from ripe.atlas.cousteau import AtlasLatestRequest

kwargs = {
    "msm_id": id,
    "probe_ids": trans_ids
}

res_success, results = AtlasLatestRequest(**kwargs).create()

if res_success:
    print(results)
def generate_fake_time_data(num_probes,start_time):
    print("GENERATING FAKE TIME DATA")
    datetime().now(tz=tzinfo(0))

def generate_fake_latency_data(num_probes,start_time):
    print("GENERATING FAKE LATENCY DATA")
def generate_fake_time_data(start_time):
    times = []
    d = datetime.now()
    for j in range(start_time, start_time+(int)(HOURS_IN_DAY*MIN_IN_HOUR/MIN_BETWEEN_REQUESTS)):
        times.append(datetime(d.year,d.month, d.day)+timedelta(0,0,0,0,(15*j)))
    return times


def generate_fake_latency_data(start_time):
    data = []
    for j in range(start_time,start_time+(int)(HOURS_IN_DAY*MIN_IN_HOUR/MIN_BETWEEN_REQUESTS)):
        data.append(random.randint(0, 200))
    return data

def test_plots_with_fake_data(num_probes):
    data = []
    for i in range(num_probes):
        fake_time_data = generate_fake_time_data(0)
        fake_latency_data = generate_fake_latency_data(0)
        d = [(fake_time_data[i],fake_latency_data[i]) for i in range(0, len(fake_time_data))]
        data.append(d)
    generate_plots(data)
GENERATE_PLOT = True

def main():
    if FETCH_IDS or TEST_GRAPHING:
        starlink_probe_ids = get_starlink_probe_ids()
        num_starlink_probes = len(starlink_probe_ids)
    if TEST_GRAPHING:
        test_plots_with_fake_data(num_starlink_probes)
    if GENERATE_PLOT:
        r = requests.get(prefix + 'measurements/'+ str(msm_id) + '/results')
        j = r.json()
        data = json_to_graph(j)
        generate_plots(data)
    

main()