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
from plot_ping import generate_plots
from datetime import datetime, tzinfo

prefix = 'https://atlas.ripe.net/api/v2/'

HOURS_IN_DAY = 24
MIN_IN_HOUR = 60

DAYS_OF_REQUESTS = 1

MIN_BETWEEN_REQUESTS = 15
S_BETWEEN_REQUESTS = MIN_BETWEEN_REQUESTS * 60
MS_BETWEEN_REQUESTS = S_BETWEEN_REQUESTS * 1000

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

def main():
    starlink__probe_ids = get_starlink_probe_ids()
    num_starlink_probes = len(starlink__probe_ids)

    fake_time_data = generate_fake_time_data(num_starlink_probes, 0)
    fake_latency_data = generate_fake_latency_data(num_starlink_probes, 0)
    generate_plots(range(1,6), [12.4,6.2,5.3,4.1,8.0])

main()