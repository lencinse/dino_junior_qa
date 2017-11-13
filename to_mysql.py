from sqlalchemy import create_engine
import pandas as pd

pdata = pd.read_pickle('data/data_anomalies.pkl')

pdata = pdata[pdata['is_anomaly']>0]
pdata = pdata.loc[:, ['ts','api_name', 'mtd', 'count_http_code_5xx', 'is_anomaly'] ]

print(pdata)

engine = create_engine('mysql://alena:alena@localhost:3306/dinotest')
pdata.to_sql(name='anomalies',con=engine,if_exists='fail',index=False)
