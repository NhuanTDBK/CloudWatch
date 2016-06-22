from service.BaseEngine import BaseEngine
from utils.auto_load import AutoLoad

loader = AutoLoad()
engine = loader.auto_load_engine_default(method='SHESD')
service = BaseEngine(engine=engine,db_name='example',measurement='vc1_2weeks', number_of_days=20)
service.work()