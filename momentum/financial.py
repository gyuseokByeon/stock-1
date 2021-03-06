
import time
import stock as stock
import tqdm as tqdm
import matplotlib.pyplot as plt
import numpy as np

DATASET_LABEL = ["TRAINING", "VALIDATING", "TESTING"]

WEEK=8
MONTH=30
QUARTER=91
YEAR=366

MINIMUM_SAMPLING_RANGE=2
STANDARD_SAMPLING_RANGE=3
MAXIMUM_SAMPLING_RANGE=5 

def normalize(matrix):
    """ MinMaxScaler to normalize matrix with high values """
    min = 10000
    max = -10000
    for val in matrix:
        if val < min:
            min = val
        elif val > max:
            max = val
        else:
            pass
    for i in range(len(matrix)):
        matrix[i] = (matrix[i] - min) / (max - min)
    return matrix, min, max
def normalize_value(value, min, max):
    return (value - min) / (max - min)
def rescale(value, min, max):
    """ Reverse of a MinMaxScaler: scales up a certain value based on a min max value """
    return (value * (max - min)) + min 

class TimeSeries:
    def __init__(self, raw):
        self.dataset_label = ""
        self.raw = raw
        self.min = 0.00
        self.max = 0.00
        self.final_close_value = self.raw[len(self.raw) - 1]
        self.sampled = []
        del self.raw[len(self.raw) - 1]
    def maximum(self):
        return self.max
    def minimum(self):
        return self.min
    def get_dataset_label(self):
        return self.dataset_label
    def get_close_value(self): # this is the labeled output of the corresponding time series data
        return self.final_close_value
    def raw_size(self):
        return len(self.raw)
    def raw_matrix(self):
        return self.raw
    def raw_datapoint(self, index):
        return self.raw[index]
    def sampled_size(self):
        return len(self.sampled)
    def sampled_datapoint(self, index):
        return self.sampled[index]
    def sampled_matrix(self):
        return self.sampled
    def append_sampled_datapoint(self, val):
        self.sampled.append(val)
    def set_dataset_label(self, label):
        self.dataset_label = label
    def set_raw_matrix(self, matrix):
        self.raw = matrix
    def set_sampled_matrix(self, matrix):
        self.sampled = matrix
    def normalize_timeseries(self):
        self.raw, self.min, self.max = normalize(self.raw)
        self.sampled, _min, _max = normalize(self.sampled)
        self.final_close_value = normalize_value(self.final_close_value, self.min, self.max)

def moving_average(timeseries, trend_window_range):
    """ Moving average analysis to detect trend in stock price variability """
    """ type(timeseries) should be "Dataset" """
    """ RETURNS: Rolling mean trend 1D matrix, a prediction value """
    trend = []
    for _range in range(0, timeseries.raw_size() - trend_window_range):
        avg = 0.00
        for i in range(_range, _range + trend_window_range):
            if i >= timeseries.raw_size():
                break
            else:
                avg += timeseries.raw_datapoint(i)
        if _range + trend_window_range < timeseries.raw_size():
            avg /= trend_window_range
        else:
            avg /= timeseries.raw_size() - _range
        trend.append(avg)
    return trend
def sampling(matrix, itr=0, loop=2, sampling_range=STANDARD_SAMPLING_RANGE):
    """ Apply after trend line computation
    samples out the first and last datapoint on a specific range of a trend line """
    if itr == loop:
        return 1
    else:
        sampled = []
        sampled.append(matrix[0])
        for _range in range(sampling_range, len(matrix) - sampling_range, sampling_range):
            sampled.append(matrix[_range])
        itr += 1
        sampling(sampled, itr, loop, sampling_range)
    return sampled
