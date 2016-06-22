import numpy as np
from outlier.BaseOutlier import BaseOutlier
import statsmodels.api as sm
import statsmodels.formula.api as smf

from pandas import Series


class STL(BaseOutlier):
    """
      Parameters
    ----------
        model : str {"additive", "multiplicative"}
            Type of seasonal component. Abbreviations are accepted.
        freq : int, optional
            Frequency of the series. Must be used if x is not a pandas
            object with a timeseries index.
        model : str {"average", "median"}
            Type of seasonal removal
        Returns
        -------
        results object
    """
    @staticmethod
    def get_attributes():
        return {
            "freq":24*60,
            "model":'addtitive',
            'mode':'median'
        }
    def __init__(self, freq=24*60, model='addtitive', mode='median'):
        self.freq = freq
        self.model = model
        self.mode = mode
        self.check_freq()

    def fit(self, data=None):
        self.data = data
        self.check_finite(data)
        if (self._is_using_pandas(data) == True):
            self.data.interpolate(inplace=True)
            self.index = data.index
        return self

    def predict(self, data=None):
        # decomfreq = freq
        res = sm.tsa.seasonal_decompose(self.data.tolist(), freq=self.freq, model=self.model)
        #     res.plot()
        random = Series(res.resid)
        mean_nan = 0
        std_nan = 0
        # random = res.resid
        if (self.mode == 'average'):
            mean_nan = np.nanmean(random)
            std_nan = np.nanstd(random)
        elif (self.mode == 'median'):
            rolling_median = random.rolling(3).median()
            mean_nan = np.nanmean(rolling_median)
            std_nan = np.nanstd(rolling_median)
        min_val = mean_nan - 4 * std_nan
        # max_val = mean(random, na.rm = T) + 4*sd(random, na.rm = T)
        max_val = mean_nan + 4 * std_nan
        position = Series(res.resid.tolist(), index=np.arange(res.resid.shape[0]))
        anomaly = position[(position > max_val) | (position < min_val)]
        # anomalyL = position[(position<min_val)]
        # anomaly = anomalyH.append(anomalyL).drop_duplicates()
        point_anomaly_idx = anomaly.index
        self.anomaly_idx = point_anomaly_idx
        points_anomaly = self.data[point_anomaly_idx]
        self.anomalies = points_anomaly
        return points_anomaly
    #
    # def fit_and_predict(self, data=None):
    #     self.fit(data)
    #     return self.predict(data)
    def fit_predict(self, data=None):
        self.fit(data)
        return self.predict(data)
    def plot(self):
        import matplotlib.pyplot as plt
        # ax = plt.subplot()
        fig, ax = plt.subplots(1, 1, sharex=True)
        ax.plot(self.data, color='red')
        ax.plot(self.anomalies, 'o')
        number_of_anomalies = self.anomalies.shape[0]
        ax.set_title("Anomaly Detection: %s" % number_of_anomalies)
        fig.tight_layout()
        return fig
