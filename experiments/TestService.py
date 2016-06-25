from service.BaseEngine import BaseEngine
from utils.auto_load import AutoLoad
from service.DataSource import DataSource
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
import uuid
import ConfigParser
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

Config = ConfigParser.ConfigParser()
cfgFile = Config.read('config.cfg')

host = Config.get('DATABASE','host')
port = Config.get('DATABASE','port')
dbname= Config.get('DATABASE','dbname')
username =  Config.get('DATABASE','username')
password = Config.get('DATABASE','password')
measurement = Config.get('DATABASE','measurement')

time_activate = Config.getint('SIMULATE','time_of_detect')

scheduler = BackgroundScheduler()
scheduler.start()
loader = AutoLoad()
engine = loader.auto_load_engine_default(method='SHESD')
# Cau hinh lai db name va measurement tro toi CSDL Influxdb
# Service tu dong load 20 ngay gan nhat de du doan anomaly
datasource = DataSource(username=username,password=password, db_name=dbname,measurement=measurement)
service = BaseEngine(engine=engine, datasource=datasource)
id_service = str(uuid.uuid4())
# service.work()
scheduler.add_job(service.work, 'interval', seconds=time_activate, id=id_service)
while True:
    i = 0