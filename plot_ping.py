import matplotlib.pyplot as plt
import matplotlib.dates as dates
import numpy
from datetime import datetime


def generate_plots(data):
  f = plt.figure(figsize=(27.6667,15.1111))
  i = 0
  for d in data:
    i += 1
    zipped_data = [list(a) for a in zip(*d)]
    x_calculations = zipped_data[0]
    y_calculations = zipped_data[1]
    plt.plot(x_calculations,y_calculations, label='Starlink Probe #'+str(i))
  
  plt.xlabel("time (UTC)")
  plt.ylabel("latency (s)")
  plt.title("Latency Over Time for RIPE Atlas Starlink Probes")
  f.legend(loc='upper right')
  plt.savefig('./plots/ping_plots/starlink_plots' + datetime.now().isoformat()+'.png')
  

