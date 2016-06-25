#!/usr/bin/python2
import os
from datetime import datetime
import time
import json
import numpy as np
import random
from influxdb import InfluxDBClient


import ConfigParser
Config = ConfigParser.ConfigParser()
cfgFile = Config.read('../config.cfg')

host = Config.get('DATABASE','host')
port = Config.get('DATABASE','port')
dbname= Config.get('DATABASE','dbname')
measurement = Config.get('DATABASE','measurement')
username =  Config.get('DATABASE','username')
password = Config.get('DATABASE','password')
time_simulate = Config.getint('SIMULATE','time_of_input_points')
client = InfluxDBClient(host, port, username, password, dbname)
client.drop_database(dbname) # 2.10 delete_database / 2.12: drop_database
client.create_database(dbname)

def convert(point):
    return [{
        "measurement": "data",
            "time": point[1],
            "fields": {
                "value": point[0],
                "anomaly": 1.0
            }
        }
    ]

def main(filename):
    json_object = None
    with open(filename) as data_file:   
        json_object = json.load(data_file)

    series = []

    for point in json_object[0]['datapoints']:
        try:
            point[0] = int(point[0])
        except Exception, e:
            point[0] = 0
            pass
        series.append([point[0], str(datetime.fromtimestamp(point[1]))])
    series = np.array(series)
    print "Batch write 2 weeks"
    for point in series[:24*60*20]:
        try:
            client.write_points(convert(point))
        except Exception, e:
            pass
    print "Simulate real time data"
    for point in series[24*60*14:]:
        time.sleep(1)
        try:
            client.write_points(convert(point))
        except Exception, e:
            pass