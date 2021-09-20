# Run_For_Life
Strive School Build Week 2 Project


![alt text](https://www.ft.com/__origami/service/image/v2/images/raw/https://d1e00ek4ebabms.cloudfront.net/production/6911fc1a-b440-4a95-b91d-00644192aff8.jpg?source=next&fit=scale-down&quality=highest&width=1067 "Logo Title Text 1")




*This program based on using AI to make life simpler.*

### THE TARGET

The purpose of this project was to produce a classification model that detects a journey type from from phone sensor readings.
    
The categories of journey we are trying to classify are;

1. On a train
2. On the road (e.g. bus/car)
3. Walking
4. Sitting still


### THE DATA

I used a set of 229151 sensor readings taken from 100's of different journeys to train our model. The data set I used can be seen [**here.**](https://www.researchgate.net/profile/Charith-Perera-2) 

![alt text](https://www.researchgate.net/profile/Charith-Perera-2/publication/234017923/figure/fig2/AS:667614586101765@1536183129256/Sensors-in-Mobile-Phones.png "Logo Title Text 1")



### WHAT I DID WITH THE DATA

I first ran some functions on the data to decide where a recording started and ended, this would prove vital
later for getting consistencies over time windows as the dataset was organised in such a way that time had lost
it's true meaning.

In later production when we take live data from a device this step will not be necessary. I did it at this stage of development to replicate sequential sensor readings as the original data sometimes is not correctly ordered.



### DATA LEAKS

My first models ran at 97-99% accuracy with no tuning, I was incredibly suspicous of our results. I isolated a new user that the model hasn't seen before we found that 'user traits' were leaking test data to our training model.

I then took the approach to isolate individual users for testing, our predictions dropped to 45% accuracy, now I had some work to do!

After taking sometime to analyze the feature importance and different combination of ML models we were able to improve this upto a whopping 85.14% over 4 classes and 97% over 3 classes.

![alt text](https://www.zivver.eu/hubfs/Data_Breach_vs.%20Data_leak_explained_zivve_blog_en.jpg "Logo Title Text 1")
