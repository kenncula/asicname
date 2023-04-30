import requests

starlink_ids='61537,60929,61113,60510,52955,52918,1004453,1005627,26834,1004876,1002827,1002750,35681,17979,20544'
arr_starlink_ids=[61537,60929,61113,60510,52955,52918,1004453,1005627,26834,1004876,1002827,1002750,35681,17979,20544]
start_date=datetime(2023, 5, 1, hour=0, minute=0, second=0)
end_date=datetime(2023, 5, 2, hour=0, minute=0, second=0)
ATLAS_API_KEY = "" #insert API_KEY_HERE


from ripe.atlas.cousteau import Ping
from ripe.atlas.cousteau import AtlasSource

ping = Ping(
    af=4,
    target="bing.com",
    description="Ping to bing.com every 15 min for a day",
    interval=900 #this sets the interval to ping every 15 minutes
    #is_oneoff=True #this is for testing,
)

source = AtlasSource(
    type="probes",
    value=starlink_ids,
    requested=len(starlink_ids)
)

from datetime import datetime
from ripe.atlas.cousteau import (
  AtlasSource,
  AtlasCreateRequest
)

atlas_request = AtlasCreateRequest(
    start_time=start_date,
    stop_time=end_date,
    key=ATLAS_API_KEY,
    measurements=[ping],
    sources=[source]
    #is_oneoff=True
)

import re
(is_success, response) = atlas_request.create()
print('measurement creation success: ' + str(is_success))
print(response)

id=re.sub("[^0-9]", "", str(response))
print("msm_id: " + id)

from ripe.atlas.cousteau import AtlasResultsRequest

kwargs = {
    "msm_id": id,
    "start": start_date,
    "stop": end_date,
    "probe_ids": arr_starlink_ids
}

res_success, results = AtlasResultsRequest(**kwargs).create()
if(res_success and is_success):
    print('result request success!')
else:
    print('result request failure')