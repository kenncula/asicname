import json
import tzdata
from datetime import datetime, timedelta, timezone

def json_to_graph(j):
    """
    json : a list of dictionaries
      dict{
      "fw":5020,
      "mver":"2.2.1",
      "lts":54,
      "dst_name":"142.250.179.206",
      "af":4,"dst_addr":"142.250.179.206",
      "src_addr":"172.24.0.2",
      "proto":"ICMP",
      "ttl":58,
      "size":64,
      "result":[
        {"rtt":44.703186},{"rtt":41.483111 {"rtt":41.936667}
        ],
      "dup":0,
      "rcvd":3,
      "sent":3,
      "min":41.483111,
      "max":44.703186,
      "avg":42.7076546667,
      "msm_id":52637483,
      "prb_id":1002289,
      "timestamp":1682445214,
      "msm_name":"Ping",
      "from":"145.224.74.30",
      "type":"ping",
      "group_id":52637483,
      "step":null,
      "stored_timestamp":1682445239
      }
    """
    #we create a dict so we can index by probe id and consolidate data

    json_obj = j
    probe_dict_avg = {}
    probe_dict_min = {}
    probe_dict_max = {}
    for probe in json_obj:
        idx = probe["prb_id"]
        data_avg = (datetime.fromtimestamp(probe["timestamp"], tz=timezone(timedelta(0,0))), probe["avg"])
        data_min = (datetime.fromtimestamp(probe["timestamp"], tz=timezone(timedelta(0,0))), probe["min"])
        data_max = (datetime.fromtimestamp(probe["timestamp"], tz=timezone(timedelta(0,0))), probe["max"])
        try:
          probe_dict_avg[idx].append(data_avg)
        except:
              probe_dict_avg[idx] = [data_avg]
        try:
          probe_dict_min[idx].append(data_min)
        except:
              probe_dict_min[idx] = [data_min]
        try:
          probe_dict_max[idx].append(data_max)
        except:
              probe_dict_max[idx] = [data_max]
    probe_dicts = (probe_dict_avg, probe_dict_min, probe_dict_max)
    return probe_dicts