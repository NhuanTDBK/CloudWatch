from service.BaseEngine import BaseEngine
from utils.auto_load import AutoLoad
from service.DataSource import DataSource

loader = AutoLoad()
engine = loader.auto_load_engine_default(method='SHESD')
# Cau hinh lai db name va measurement tro toi CSDL Influxdb
# Service tu dong load 20 ngay gan nhat de du doan anomaly
datasource = DataSource(db_name='example',measurement='vc1_2weeks')
service = BaseEngine(engine=engine,datasource=datasource, number_of_days=20)
service.work()