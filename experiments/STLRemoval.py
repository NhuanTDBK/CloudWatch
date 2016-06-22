import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas as pd
import matplotlib.pyplot as plt
from outlier.STL import STL

from outlier.SHESD import SHESD
#
dat = pd.read_csv('../data/vc_3.json_remake',index_col=0,parse_dates=True)
# decomfreq = 24*60
# estimator = SeasonalOutlier(freq=decomfreq,model='multiplicative')
# estimator.fit_and_predict(dat.points)
# ax = estimator.plot()
# plt.show()
# res = sm.tsa.seasonal_decompose(dat.points.interpolate().tolist(),freq=decomfreq, model='addtitive')
estimator = SHESD(max_anoms=0.02,direction='both')
estimator.fit_predict(dat.points)
f = estimator.plot()
print estimator.produce()
plt.show()