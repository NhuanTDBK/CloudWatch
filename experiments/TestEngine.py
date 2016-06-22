from service.BaseEngine import BaseEngine
from utils.auto_load import AutoLoad
import pandas as pd
import matplotlib.pyplot as plt

loader = AutoLoad()
engine = loader.auto_load_engine_default(method='SHESD')
dat = pd.read_csv('../data/vc_1.json_remake',index_col=0,parse_dates=True)
engine.fit_predict(data=dat.points)
engine.plot()
plt.show()