from service.BaseEngine import BaseEngine
from utils.auto_load import AutoLoad
import pandas as pd
import matplotlib.pyplot as plt
from perioddetection import autoperiod
loader = AutoLoad()
engine = loader.auto_load_engine_default(method='SHESD')
dat = pd.read_csv('../data/dataset1/9.json_remake',index_col=0,parse_dates=True)
engine.longterm = True;
engine.piecewise_median_period = 7;
engine.max_anoms = 1/200.0
engine.fit(data=dat.points)
print autoperiod.period_detect(engine.data,segment_method = "topdownsegment")
# engine.fit_predict(data=dat.points[:-30])
# engine.plot()
# plt.show()
