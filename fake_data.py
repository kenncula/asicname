import random
from datetime import datetime, tzinfo,timedelta


HOURS_IN_DAY = 24
MIN_IN_HOUR = 60

DAYS_OF_REQUESTS = 1

MIN_BETWEEN_REQUESTS = 15
S_BETWEEN_REQUESTS = MIN_BETWEEN_REQUESTS * 60
MS_BETWEEN_REQUESTS = S_BETWEEN_REQUESTS * 1000


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