from outlier.BaseOutlier import BaseOutlier
from pyculiarity import detect_ts
import numpy as np
from pandas import DataFrame, Series, to_datetime
from pandas.tseries.index import DatetimeIndex
class SHESD(BaseOutlier):
    @staticmethod
    def get_attributes():
        return {
            "max_anoms":0.02,
            "direction":"both",
            "alpha":0.05,
            "threshold":None,
            "piecewise_median_period_weeks":2
        }
    def __init__(self, max_anoms=0.02, direction='both', alpha=0.05, only_last=None, threshold=None,
                 e_value=False, longterm=True,
                 piecewise_median_period=3, plot=False,
                 y_log=False, xlabel = '', ylabel = 'count',
                 title=None, verbose=False, period = None):
        self.max_anoms = max_anoms
        self.direction = direction
        self.alpha = alpha
        self.only_last = only_last
        self.threshold = threshold
        self.e_value = e_value
        self.longterm = longterm
        self.piecewise_median_period = piecewise_median_period
        # self.plot=plot
        self.y_log = y_log
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title
        self.verbose = verbose
        self.custom_period = period
    def convert_twitter_format(self,data=None):
        columns = ["timestamp", "points"]
        b = DataFrame(index=np.arange(data.shape[0]), columns=columns)
        b[columns[0]] = data.index
        b[columns[1]] = data.tolist()
        return b
    def fit(self, data=None):
        self.data = self.convert_twitter_format(data)
        self.check_finite(data)
        if (self._is_using_pandas(data) == True):
            self.data.interpolate(inplace=True)
        if(isinstance(data.index,DatetimeIndex)):
            self.index = to_datetime(self.data['timestamp'])
        else:
            self.index = data.index
        return self
    def predict(self,data=None):
        results = detect_ts(data, max_anoms=self.max_anoms,
                            direction=self.direction, alpha=self.alpha, only_last=self.only_last,
                            threshold=self.threshold, e_value=self.e_value, longterm = self.longterm,
                            piecewise_median_period=self.piecewise_median_period, custom_period=self.custom_period)
        anoms = results['anoms']
        self.anomaly_idx = anoms.index
        self.anom_val = anoms['anoms']
        return anoms
    def fit_predict(self, data=None):
        self.fit(data)
        return self.predict(self.data)
    def plot(self):
        import matplotlib.pyplot as plt
        f, ax = plt.subplots(1, 1)
        ax.plot(self.data['timestamp'], self.data['value'], 'b')
        ax.plot(self.anomaly_idx, self.anom_val, 'ro')
        ax.set_title('Detected Anomalies')
        ax.set_ylabel('Count')
        f.tight_layout()
        return f
