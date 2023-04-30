class DataNode:
    def __init__(self, med,avg,min,max,timestamp):
        self._med = med
        self._avg = avg
        self._min = min
        self._max = max
        self._timestamp = timestamp

    
    def get_med(self):
        return self._med
      
    def set_med(self, med):
        self._med = med

    def get_avg(self):
        return self._avg
      
    def set_avg(self, avg):
        self._avg = avg

    def get_min(self):
        return self._min
      
    def set_min(self, min):
        self._min = min

    def get_max(self):
        return self._max
      
    def set_max(self, max):
        self._max = max

    def get_timestamp(self):
        return self._timestamp
      
    def set_timestamp(self, timestamp):
        self._timestamp = timestamp


    def __str__(self):
        return "Median = " + str(self._med) + ", Average = " + str(self._avg) + ", Min = " + str(self._min) + ", Max = " + str(self._max) + ", Timestamp = " + str(self._timestamp)
    