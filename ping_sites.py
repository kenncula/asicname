from ripe.atlas.cousteau import Ping
from ripe.atlas.cousteau import AtlasSource
from datetime import datetime
from ripe.atlas.cousteau import (
  AtlasSource,
  AtlasCreateRequest
)
from ripe.atlas.cousteau import AtlasLatestRequest
import re
import json

f = open('client_secret.json')
j = json.load(f)
ATLAS_API_KEY = j["Google_Ping_API_KEY"]

def ping_google(ids):
    starlink_ids = ids
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

    atlas_request = AtlasCreateRequest(
        key=ATLAS_API_KEY,
        measurements=[ping],
        sources=[source],
        is_oneoff=True
    )


    (is_success, response) = atlas_request.create()
    id=re.sub("[^0-9]", "", str(response))
    print("msm_id:" + id)

    kwargs = {
        "msm_id": id,
        "probe_ids": trans_ids
    }

    res_success, results = AtlasLatestRequest(**kwargs).create()

    if res_success:
        print(results)
