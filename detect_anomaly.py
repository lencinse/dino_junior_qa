import pandas as pd
import numpy as np
from scipy.stats import norm, poisson


pdata = pd.read_pickle('data/data_count.pkl')


anomaly_col_name = 'is_anomaly'
pdata[anomaly_col_name] = 0


# foreach (api_name, mtd) group
for name, group in pdata.groupby(['api_name', 'mtd']):
    print(name)
    group.reset_index(level=0, inplace=True)
    group_data = group.as_matrix(columns=['index', 'count_http_code_5xx'])
    
    group_data = group_data[group_data[:,-1]>0]

    if group_data[:,-1].sum() < 10:
        # to small count of points for some statistics estimation
        # mark as -1
        group_data[:,-1] = -1
    else:
        # perform normal distribution fiting
        # to do: poisson is more suitable in this case
        # https://ru.wikipedia.org/wiki/%D0%A0%D0%B0%D1%81%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5_%D0%9F%D1%83%D0%B0%D1%81%D1%81%D0%BE%D0%BD%D0%B0
        
        sig = np.std(group_data[:,-1])
        mean= np.mean(group_data[:,-1])
        group_data[:,-1] = (group_data[:,-1] - mean > 3*sig).astype(int)
        
    for row in group_data:
        pdata.at[row[0], anomaly_col_name] = row[-1]
    
print(pdata[pdata[anomaly_col_name]>0].head())
pdata.to_pickle('data/data_anomalies.pkl')
