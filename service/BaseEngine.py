# import pandas as pd
from influxdb import DataFrameClient
from influxdb.resultset import ResultSet
from datetime import datetime
from service.DataSource import DataSource
import numpy as np
from outlier.BaseOutlier import BaseOutlier
from perioddetection import autoperiod
from utils.auto_load import AutoLoad

class BaseEngine(object):
    def check_influxdb_connected(self,host,port,username,password,db_name):
        client = DataFrameClient(host, port, username, password,db_name)
        result = True
        try:
            client.get_list_database()
            print "Connect to database server"
        except:
            result = False
            print "Cannot connect. Please check configuration server"
        return result
    def __init__(self,engine=None, datasource = None,interval=20,number_of_days = 30):

        if(datasource==None):
            raise Exception("Please plugin datasource")
        host,port,username,password,db_name,measurement = datasource._return()
        self.db_name = db_name
        self.measurement = measurement
        self.interval = interval
        self.number_of_days = number_of_days
        self.status = "INIT"
        self.cursor = datetime.now()
        self.number_of_anomalies = 0
        if isinstance(engine,BaseOutlier) == False:
            print "Please plug in Engine instance of BaseOutlier"
            # raise ValueError("Please plug in Engine instance of BaseOutlier")
        else:
            print "Engine is already"
            self.engine = engine
        if self.check_influxdb_connected(host,port,username,password,db_name):
            self.client_api = DataFrameClient(host, port, username, password,db_name)
            self.datasource = datasource

        # self.engine =
    # def query_analyzed(self):
    #     print "Get latest time series points"
    #     query_set = 'select value from %s order by time desc limit %s ;'%(self.measurement,self.number_of_days*24*60)
    #     result = self.client_api.query(query_set)[self.measurement]
    #     return result
    # def query_all(self):
    #     print "Get latest time series points"
    #     query_set = 'select value from %s limit 10000;'%(self.measurement)
    #     result = self.client_api.query(query_set)[self.measurement]
    #     return result
    def fit_predict(self,data=None):
        self.engine.fit_predict(data)
        return self.engine.produce()
    # def update_db(self,data):
    #     result = False
    #     if self.engine._is_using_pandas(data):
    #         try:
    #             result = self.client_api.write_points(data,self.measurement)
    #         except Exception as e:
    #             print e.message
    #     return result
    def check_period(self):
        print "Checking period..."
        loader = AutoLoad()
        a = self.engine.convert_twitter_format(self.datasource.query_all().value)
        period = np.array(autoperiod.period_detect(a, segment_method="topdownsegment"))
        if period.size == 0:
            # self.engine = loader.auto_load_engine_default(method='KMeansBase')
            self.engine.use_period = False
        else:
            self.engine.custom_period = period.min()
    def work(self):
        print "Start detecting..."
        data = self.datasource.query_analyzed()
        sorted_res = data.tz_convert(None).sort(ascending=True).drop_duplicates(keep='first')
        ano_lbl = self.engine.fit_predict(sorted_res['value'])
        output = self.engine.produce()
        result = self.datasource.update_db(output)
        # output = self.engine._is_anomaly_point()
        # if output != None:
        #     print "Anomaly Detection!"
        #     self.number_of_anomalies += 1
        #     result = self.update_db(output)
        # if result:
        #     print "Successfully detect anomaly"
        # return result



