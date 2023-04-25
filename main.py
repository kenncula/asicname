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

prefix = 'https://atlas.ripe.net/api/v2/'

def get_starlink_ids():
    tags = 'starlink'
    status = 'Connected'
    is_public = True

    r = requests.get(prefix + 'probes/?tags=' + tags + '&is_public=' + str(is_public) + '&status_name=' + status)

    j = r.json()

    ids = []

    for res in j['results']:
        ids.append(res['id'])
    return ids

starlink_ids=get_starlink_ids()
print(starlink_ids)

from ripe.atlas.cousteau import Ping
from ripe.atlas.cousteau import AtlasSource

ping = Ping(
    af=4,
    target="google.com",
    description="Ping Test",
    #interval=900,
    is_oneoff=True
)

source = AtlasSource(
    type="probes",
    value="19983",
    requested=1
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
print(id)
print(is_success)
print(response)


from ripe.atlas.cousteau import AtlasResultsRequest

kwargs = {
    "msm_id": id,
    "start": datetime(2023, 4, 25),
    "stop": datetime(2023, 4, 26),
    "probe_ids": "19983"
}

res_success, results = AtlasResultsRequest(**kwargs).create()

from ripe.atlas.sagan import PingResult

my_result = PingResult(results)


print(my_result.rtt_median)

if res_success:
    print(results)
