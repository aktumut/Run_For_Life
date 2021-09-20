import numpy as np
import pandas as pd
import time
import random
from joblib import load, dump
import get_data as gt
import os
from csv import reader
import sys

model = load('bw2_model.joblib');

magnitudes = []
predictions = []
n_preds = 3

with open(sys.argv[1]) as obj:

    csv_reader = reader(obj)
    next(csv_reader, None)

    for row in csv_reader:
        
        row = [float(i) for i in row]

        row = np.array(row)

        if len(magnitudes) < 10:
            magnitudes.append(gt.magnitude(row))
        else:
            mi, ma, st = gt.get_min_max_std(magnitudes)
            X = np.array([mi, ma, st])
            magnitudes = []

            predictions.append(model.predict([X]))

            if len(predictions) == 5:
                walk = 0
                stand = 0
                for p in predictions:
                    if p == 0:
                        stand += 1
                    elif p == 1:
                        walk += 1
                
                if walk > n_preds:
                    open('walking.txt', 'a').close()
                else:
                    if os.path.isfile('walking.txt'):
                        os.remove('walking.txt')
                
                if stand > n_preds:
                    open('still.txt', 'a').close()
                else:
                    if os.path.isfile('still.txt'):
                        os.remove('still.txt')
                
                predictions.remove(predictions[0])

                time.sleep(1/int(sys.argv[2]))


    if os.path.isfile('walking.txt'):
        os.remove('walking.txt')
    if os.path.isfile('still.txt'):
        os.remove('still.txt')
