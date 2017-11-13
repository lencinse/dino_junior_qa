import pandas as pd
import numpy as np

import time
from datetime import datetime
from datetime import timedelta


pdata = pd.read_pickle('data/data.pkl')

#add column for metric
metric_col_name = 'count_http_code_5xx'
pdata[metric_col_name] = -1


j = pdata.columns.get_loc('count_http_code_5xx')


# vectorize timestamp function
def to_timstamp(datetime_obj):
    return datetime_obj.timestamp()
v_to_timstamp = np.vectorize(to_timstamp)
#


# foreach (api_name, mtd) group
for name, group in pdata.groupby(['api_name', 'mtd']):
    print(name)
    
    # Slicing in pandas doesn't work on indexes that are not either monotonic increasing or monotonic decreasing
    # preserve index
    group.reset_index(level=0, inplace=True)
    # and convert to numpy array
    group_data = group.as_matrix(columns=['index', 'ts', 'cod'])


    total_count_5xx = int(group_data[:,-1].sum())
    if total_count_5xx==0:
        continue
    print('detected 5xx requests: ', total_count_5xx)

    # calc 15 min ahead
    timeframe_stop = group_data[:,1] + timedelta(minutes = 15)
    # convert date time to timestamps in sec
    ts = v_to_timstamp(group_data[:, 1])
    ts_stop = v_to_timstamp(timeframe_stop)
    

    COUNT=0 # just for check

    # iterate each 15 min interval
    i = 0 
    while i < ts.shape[0]:
        stop_i = np.argmax(ts[i:]-ts_stop[i]>=0)
        stop_i+=i
        # i -- start time
        # stop_i -- 15 min from start time
        
        if ts[stop_i] == ts_stop[i] or stop_i==i:
            stop_i+=1   

        # count of 5xx codes in interval [i, stop_i]
        count = int(group_data[i:stop_i, -1].sum())
        COUNT+=count
        pdata.at[group_data[i, 0], metric_col_name] = count
        # moove to the next interval
        i=stop_i
    
    print('processed 5xx requests: ', COUNT)


pdata = pdata[pdata['count_http_code_5xx']>=0]  
print(pdata.head())
    
pdata.to_pickle('data/data_count.pkl')
