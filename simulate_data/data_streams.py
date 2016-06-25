#!/usr/bin/python2
import os
from datetime import datetime
import time
import json
import random
from influxdb import InfluxDBClient

ip = '127.0.0.1'
port = 8086
username = 'root'
password = 'root'
dbname = 'test'

client = InfluxDBClient(ip, port, username, password, dbname)
client.drop_database('test') # 2.10 delete_database / 2.12: drop_database
client.create_database('test')

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

    for point in series:
        time.sleep(1)
        try:
            client.write_points(convert(point))
        except Exception, e:
            pass
    
if __name__ == '__main__':
    main(os.path.abspath('../data/dataset1/14.json'))