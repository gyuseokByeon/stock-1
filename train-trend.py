#!/usr/bin/env python3

import os
import tqdm as tqdm
from stock import upload
from service import download_stock, git_update
from financial import QUARTER, MONTH, STANDARD_SAMPLING_RANGE
from financial import partition_time_series, moving_average, sampling
from model import KerasTrainer, Model

if __name__ == "__main__":
    os.system('clear')
    path, id = download_stock()
    data = upload(path)
    dataset = partition_time_series(data, QUARTER, 0)
    
    loop = tqdm.tqdm(total = len(dataset), position = 0, leave = False)
    for timeseries in dataset:
        loop.set_description('Time series trend line analysis/sampling... ' .format(len(dataset)))
        matrix = moving_average(timeseries, MONTH)
        matrix = sampling(matrix, 0, 2, STANDARD_SAMPLING_RANGE)
        timeseries.set_sampled_matrix(matrix)
        timeseries.normalize_timeseries()
    loop.update(1)
    print("\nCompleted timeseries analysis")
    loop.close()
    
    training_input = []
    training_output = []
    validation_input = []
    validation_output = []

    training_break_point = int((len(dataset) * 60) / 100)

    for i in range(0, len(dataset) - 2):
        if i < training_break_point - 2:
            training_input.append(dataset[i].sampled_matrix())
            training_output.append(dataset[i + 2].sampled_matrix())
        else:
            validation_input.append(dataset[i].sampled_matrix())
            validation_output.append(dataset[i + 2].sampled_matrix())
    
    try:
        f = open("'Trend Models'/" + id + ".h5", "r")
        m = Model(id)
    except IOError:
        m = KerasTrainer()
        m.feed(training_input, training_output, validation_input, validation_output)
        m.train(True, "'Trend Models'", 10, 32)
    git_update()
