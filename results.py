'''
This file just asks for msm_id as input and outputs the results to results.json for necessary use
'''

from datetime import datetime
start_date=datetime(2023, 5, 1, hour=0, minute=0, second=0)
end_date=datetime(2023, 5, 2, hour=0, minute=0, second=0)
arr_starlink_ids=[61537,60929,61113,60510,52955,52918,1004453,1005627,26834,1004876,1002750,35681,17979,20544]

from ripe.atlas.cousteau import AtlasResultsRequest

id=input("Please give the measurement id:\n")

kwargs = {
    "msm_id": id,
    "start": datetime(2023, 4, 30, hour=0,minute=0,second=0),
    #"start": start_date,
    #"stop": end_date,
    "probe_ids": arr_starlink_ids
}

res_success, results = AtlasResultsRequest(**kwargs).create()
file=open("results.json", results)
print("Results outputted to results.json")