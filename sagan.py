import requests,json, node
from ripe.atlas.sagan import PingResult
source = "https://atlas.ripe.net/api/v2/measurements/52637483/results/"
response = requests.get(source)
result = json.loads(response.text)

#dictionary of probes
probe_dict = {}

#Loop through list of dictionaries
for dict in result:
   #Find ping results
    ping_result = PingResult(dict)

    #Collect data
    probe_id = dict['prb_id']
    med = ping_result.rtt_median
    avg = ping_result.rtt_average
    min = ping_result.rtt_min
    max = ping_result.rtt_max
    timestamp = dict['timestamp']

    #Organize into node
    data = node.DataNode(med,avg,min,max,timestamp)

    #checks if probe_id already has list of data
    if probe_dict.get(probe_id):
        probe_dict[probe_id].append(data)
    else:
        probe_dict[probe_id] = [data]



#Check each datanode for each probe
for key in probe_dict.keys():
    for value in probe_dict[key]:
        print(str(key) + ' // ' + str(value))

#Open and write into a file
output = open("probe_data", "a")
for key in probe_dict.keys():
    for value in probe_dict[key]:
        output.write(str(key) + ' // ' + str(value))
        output.write("\n")
output.close()