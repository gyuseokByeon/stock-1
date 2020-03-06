#!/usr/bin/env python3

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import time
import model as model
import tqdm as tqdm
from stock import upload
from service import graph, download_stock, partition_time_series, git_update
from financial import WEEK, MONTH, QUARTER, YEAR
from financial import MINIMUM_SAMPLING_RANGE, STANDARD_SAMPLING_RANGE, MAXIMUM_SAMPLING_RANGE
from financial import sampling, moving_average

os.system('clear')
print("Running ./train.py for generating/updating model")
time.sleep(2)
os.system('clear')

if __name__ == "__main__":
    while True:
        # use service module to download stock from YAHOO
        # downloaded stock will be saved as "Database/stock.csv"
        csv, id = download_stock()
        print("\nDownloaded ", id, " historical stock data [PATH=Database/stock.csv]")

        stock = upload(csv, 1, True)
        dataset = partition_time_series(stock, QUARTER) # each time series will be a quarter-long (90 datapoints)

        # compute trend line of each time series
        loop = tqdm.tqdm(total = len(dataset), position = 0, leave = False)
        for timeseries in dataset:
            loop.set_description('Time series trend line analysis/sampling... ' .format(len(dataset)))
            matrix = moving_average(timeseries, MONTH)
            matrix = sampling(matrix, 0, 2, STANDARD_SAMPLING_RANGE)
            timeseries.set_sampled_matrix(matrix)
            timeseries.normalize_timeseries()
            loop.update(1)
        print("\nCompleted trend line analysis")
        loop.close()

        # check if there is an existing model for the corresponding stock ID
        # if model exists, load existing model and train on it (model.Model: update())
        # if not, create new model (model.KerasTrainer)
        try:
            f = open("Models/" + id + "_model.h5", "r")
            m = model.Model(id, "PREDICTION_MODEL")
            m.update(dataset, True, 10, 32)
            f.close()
        except IOError:
            m = model.KerasTrainer(dataset, id.lower(), "PREDICTION_MODEL")
            m.train("Models", True, 10, 32)
        git_update()
        print("\n\n\n")