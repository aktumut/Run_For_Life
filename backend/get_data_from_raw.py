from sys import argv
import numpy as np
import pandas as pd
import os
import sys

root_dir = sys.argv[1]  
sensor = sys.argv[2]
data_list = []
activity_dict = {'Walking': 1, 'Still': 0, 'Car': 2, 'Train': 4, 'Bus': 3}

def get_sensor_data_from_file(raw_file, sensor):
    
    raw_list = []

    with open(raw_file, 'r', errors='ignore') as fp:
        buffer = fp.readlines()

        for line in buffer:
            sensor_reading = line.split(',')[1].split('.')[-1]
            if  sensor_reading == sensor:
                line = line.replace('\n', '')
                data = line.split(',')[2:]
                time = line.split(',')[0]
                raw_list.append(time)
                for i, d in enumerate(data):
                    raw_list.append(data[i])
    
    raw_list = np.array(raw_list)
    raw_list = raw_list.reshape(raw_list.shape[0] // (len(data) + 1), len(data) + 1)
    return raw_list

def magnitude(vector):
    return np.sqrt((vector**2).sum())

def get_min_max_std(a):
    a = np.array(a)
    return np.min(a), np.max(a), np.std(a)

def get_user_and_activity(raw_file):

    user = raw_file.split('_')[1]
    activity = raw_file.split('_')[2]

    return user, activity

def get_sensors_names(raw_file):

    sensors_list = []
    with open(raw_file, 'r', errors='ignore') as fp:
        buffer = fp.readlines()

        for line in buffer:
            sensor_name = line.split(',')[1]
            if  sensor_name.split('.')[0] == 'android' or sensor_name == 'sound':
                sensor_name = sensor_name.split('.')[-1]
                sensors_list.append(sensor_name)
    sensors_list = set(sensors_list)
    return sensors_list


for data_dir in os.scandir(root_dir):
    if data_dir.name[0] == 'U':
        for f in os.scandir(data_dir):
            if f.name[-3:] == 'csv':
                raw_f = root_dir + data_dir.name + os.sep + f.name
                user, activity = get_user_and_activity(raw_f)
                raw_sensor_data = get_sensor_data_from_file(raw_f, sensor)
                for data in raw_sensor_data:
                    data_list.append([user, float(data[0]) , float(data[1]), float(data[2]), activity_dict[activity]])

df = pd.DataFrame(data_list, columns=['user', 'accelerometer_min', 'accelerometer_max', 'accelerometer_std', 'target'])

df.to_csv(root_dir + sensor + '_complete_data.csv')
