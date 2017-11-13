#### prerequisite:
python3, panads, numpy, sqlalchemy

#### 1. Download raw data
 - download csv from https://drive.google.com/file/d/0B8K6jIyGsfV-VGs1VkU1cnJ0NUk/view?usp=sharing and save it to data/raw_data.csv
#### 2. Preprocessing of raw data
```sh
$ python3 load_csv.py
```
 - wait while the csv-file will be loaded into pandas data frame and some preprocessing will be completed
 -  the result will be saved to data/data.pkl
#### 3. Calculating of metric
```sh
$ python3 count_metric.py
```
 - wait while count of 5xx codes will be calculated for each (api_name,http_method) pair in 15 min intervals
 -  the result will be saved to data/data_count.pkl

#### 4. Detect of anomalies
```sh
$ python3 detect_anomaly.py
```
 - wait while anomaly based on 3*sigma rule will be estimated
 - the result  will be saved to data/data_anomalies.pkl

> NOTE, that normal distribution is not accurate for this case while metric is always possitive. Moreover, [the Poisson distribution](https://en.wikipedia.org/wiki/Poisson_distribution) is more suitable since it corresponds to the number of events occurring in a fixed interval of time.

#### 4. Upload results to MySQL
```sh
$ python3 to_mysql.py
```
 - change connection string to the server and wait while SQLAlchemy upload data frame from step 3 into MySQL table
