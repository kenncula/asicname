import matplotlib.pyplot as plt
import matplotlib.dates as dates
import numpy
from datetime import datetime


def generate_plots(time_lists,latency_lists):
  for i in range(len(time_lists)):
    plt.plot(time_lists[i],latency_lists[i])
  plt.show()
