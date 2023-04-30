import requests
import json

prefix = 'https://atlas.ripe.net/api/v2/'

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