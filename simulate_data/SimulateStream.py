import os
import time
from influxdb import InfluxDBClient, DataFrameClient
from utils.auto_load import AutoLoad

import pandas as pd

import ConfigParser
Config = ConfigParser.ConfigParser()
cfgFile = Config.read('../config.cfg')

host = Config.get('DATABASE','host')
port = Config.getint('DATABASE','port')
dbname= Config.get('DATABASE','dbname')
measurement = Config.get('DATABASE','measurement')
username =  Config.get('DATABASE','username')
password = Config.get('DATABASE','password')
time_simulate = Config.getint('SIMULATE','time_of_input_points')
number_of_days = 15
client = InfluxDBClient(host, port, username, password, dbname)
client.drop_database(dbname) # 2.10 delete_database / 2.12: drop_database
client.create_database(dbname)

def convert(point):
    return [{
        "measurement": measurement,
            "time": point[1],
            "fields": {
                "value": point[0],
                "anomaly": 1.0
            }
        }
    ]
loader = AutoLoad()
engine = loader.auto_load_engine_default(method='SHESD')

client = DataFrameClient(host, port, username, password, dbname)
client.drop_database(dbname) # 2.10 delete_database / 2.12: drop_database
client.create_database(dbname)
print "Batch Inserting 2 weeks"
dat = pd.read_csv('../data/vc_2.json_remake',index_col=0,parse_dates=True)
dat[dat.columns[1]] = dat.index
client = DataFrameClient(database=dbname)
new_dat = engine.convert_to_influx_format(dat.points).interpolate()

client.write_points(new_dat[:number_of_days*24*60],measurement)
client = InfluxDBClient(host=host,port=port,username=username,password=password,database=dbname)

print "Simulate real time data"
for k,v in dat[number_of_days*24*60:].iterrows():
    print v[1]
    client.write_points(convert(v))
    print "Push...!"
    time.sleep(10)

