from service.BaseEngine import BaseEngine
from utils.auto_load import AutoLoad
import pandas as pd
import matplotlib.pyplot as plt
from perioddetection import autoperiod
loader = AutoLoad()
engine = loader.auto_load_engine_default(method='KMeansBase')
dat = pd.read_csv('../data/dataset1/17.json_remake',index_col=0,parse_dates=True)

engine.longterm = True;
engine.use_period = False
engine.piecewise_median_period = 4;
engine.max_anoms = 1/100.0
# engine.use_period = False
engine.fit(data=dat.points)
# print autoperiod.period_detect(engine.data)
# try:
#     engine.custom_period = np.min(autoperiod.period_detect(engine.data,segment_method = "slidingwindowsegment"))
# except:
#     pass
# print engine.custom_period

engine.fit_predict(data=dat.points)
engine.plot()
plt.show()
