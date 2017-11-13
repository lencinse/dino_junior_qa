import pandas as pd
import numpy as np


pdata = pd.read_csv('data/raw_data.csv')
print('csv file is loaded')

print('max code error: ', pdata['cod'].max())
print('mix code error: ', pdata['cod'].min())


# convert datetime strings to datetime objects
ts = pd.to_datetime(pdata['ts'])
pdata['ts'] = ts


#does code correspond to 5xx
pdata['cod'] = pdata['cod']//100
pdata['cod'] = pdata['cod'] == 5


#check order of time stamps and sort data frame
print('is sorted: ', pdata['ts'].is_monotonic)
pdata = pdata.sort_values('ts')
print('is sorted: ', pdata['ts'].is_monotonic)

#save preprocessed data frame
pdata.to_pickle('data/data.pkl')

print('done')