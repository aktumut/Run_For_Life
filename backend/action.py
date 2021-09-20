import numpy as np
import pandas as pd
import time
import random
from joblib import load, dump
import get_data as gt
import os
from csv import reader

walking = False
walked = False

still = False
stalled = True

time_walked = 0
time_still = 0

while True:
    print('                                                           ', end='\r')

    if os.path.isfile('walking.txt'):

        walked = True
        walking = True
        start_walk = time.time()
        
        while walking == True:
            print('walk...', end='\r')
            if not os.path.isfile('walking.txt'):
                walking = False
        end_walk = time.time()
        time_walked += end_walk - start_walk
    
    elif os.path.isfile('still.txt'):
        stalled = True
        still = True
        start_still = time.time()
        
        while still == True:
            print('staying still...', end='\r')
            if not os.path.isfile('still.txt'):
                still = False
                time_still += time.time() - start_still
                if time_still > 5:
                    print('Take a walk, you are standing still for too much time', end='\r')
                    time_still = 0
                    time.sleep(3)

    else:
        if walked == True:
            start_idle = time.time()
            while not os.path.isfile('walking.txt'):
                end_idle = time.time()
                if end_idle - start_idle > 5:
                    walked = False
                    print(f'you walked for {round(time_walked, 0)} minutes', end='\r')
                    time_walked = 0
                    time.sleep(2)
                    break

