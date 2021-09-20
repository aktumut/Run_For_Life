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
            # scalar_sensors = ['sound', 'light']
            sensor_reading = line.split(',')[1].split('.')[-1]
            if  sensor_reading == sensor:
                line = line.replace('\n', '')
                data = line.split(',')[2:]
                time = line.split(',')[0]
                raw_list.append(time)
                for i, d in enumerate(data):
                    raw_list.append(data[i])
    # return [[float(comp) for comp in vector] for vector in raw_list]
    raw_list = np.array(raw_list)
    raw_list = raw_list.reshape(raw_list.shape[0] // (len(data) + 1), len(data) + 1)
    return raw_list

def get_activity_data(root, user, activity, data_list):

    for directory in os.scandir(root):
        if directory.is_dir() and directory.name[0] != '.':
            if directory.name == user:
                for file_ in os.scandir(directory):
                    if file_.is_file() and file_.name.split('_')[2] == activity:
                        data_list = get_sensor_data_from_file(file_, sensor)
    
    return data_list

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
    sensors_list = [sensor for sensor in sensors_list]
    return sensors_list

def create_df_from_data_list(data_list, df_name):
    df = pd.DataFrame(data_list)
    for col in df.columns:
        if col != 0:
            df[col] = df[col].astype(float)
        else:
            df[col] = df[col].astype(int).abs()

    
    df.columns = [f'{df_name}#{col}' if i != 0 else 'time' for i, col in enumerate(df.columns)]
    return df




def magnitude(vector):
    return np.sqrt((vector**2).sum())

def get_min_max_std(a):
    a = np.array(a)
    return np.min(a), np.max(a), np.std(a)

def get_user_and_activity(raw_file):

    user = raw_file.split('_')[1]
    activity = raw_file.split('_')[2]

    return user, activity

# for data_dir in os.scandir(root_dir):
#     if data_dir.name[0] == 'U':
#         for f in os.scandir(data_dir):
#             if f.name[-3:] == 'csv':
#                 raw_f = root_dir + data_dir.name + os.sep + f.name
#                 user, activity = get_user_and_activity(raw_f)
#                 raw_sensor_data = get_sensor_data_from_file(raw_f, sensor)
#                 for data in raw_sensor_data:
#                     data_list.append([float(data[0][0]), user, float(data[1][0]) , float(data[1][1]), float(data[1][2]), activity_dict[activity]])

# df = pd.DataFrame(data_list, columns=['user', f'{sensor}_x_axis', f'{sensor}_y_axis', f'{sensor}_z_axis', 'target'])

# df.to_csv(root_dir + sensor + '_raw_data.csv')

# Building the cleaned dataframe step-by-step


sens = get_sensors_names(file_name) # file name will be created looping through all the directories

all_data = pd.DataFrame({'time': []})
for s in sens:
    vars()[s] = get_sensor_data_from_file(file_name, s)  
    vars()[s] = create_df_from_data_list(vars()[s], s)
    all_data = pd.merge(all_data, vars()[s], on='time', how='outer', sort=True)
all_data['user'] = user
all_data['activity'] = file_name.split('_')[-2]
