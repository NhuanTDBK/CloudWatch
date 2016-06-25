__doc__ = 'Base Class for Outlier estimator'
from statsmodels.compat.python import lmap, range, iteritems
import numpy as np
from pandas import Series, DataFrame, WidePanel, to_datetime
from pandas.tseries.index import DatetimeIndex
import abc
class BaseOutlier(object):
    def getFormat(self):
        return [    
            "value",
            "anomaly"
        ]

    @staticmethod
    def get_attributes():
        return {

        }
    def __init__(self, **kwargs):
        for key, value in iteritems(kwargs):
            setattr(self, key, value)
    def check_finite(self,data):
        result = True
        if not np.all(np.isfinite(data)):
            result = False
        return result
            # raise ValueError("This function does not handle missing values")

    def _is_using_pandas(self,endog):
        klasses = (Series, DataFrame, WidePanel)
        return (isinstance(endog, klasses))

    def check_freq(self):
        result = True
        if(self.freq is None):
            result = False
        return result
            # raise ValueError("You must specify a freq or x must be a "
            #              "pandas object with a timeseries index")

    """
        Parameters
      ----------
          data : pandas type (Series, DataFrame)
                Original time series
          anomaly_idx: Series or numpy darray
                Index of anomaly points
          Returns
          -------
                Array of label anomaly
    #   """
    def produce(self):
        anomaly_idx = self.anomaly_idx
        ano_lbl = Series(np.ones(self.data.shape[0]), index=self.index)
        if(isinstance(anomaly_idx,DatetimeIndex)):
            ano_lbl.ix[anomaly_idx] = 0.
        else:
            ano_lbl.iloc[anomaly_idx] = 0
        new_data = DataFrame(index=self.index, columns=self.getFormat())
        if type(self.data) is DataFrame:
            new_data['value'] = self.data['value'].tolist()
        elif type(self.data) is Series:
            new_data['value'] = self.data.tolist()

        # new_data['time'] = self.index.tolist()
        new_data['anomaly'] = ano_lbl
        return new_data
    @abc.abstractmethod
    def fit_predict(self, data=None):
        """Retrieve data from the input source and return an object."""
        raise NotImplementedError()
    def convert_to_influx_format(self,data=None):
        if isinstance(data,Series) == False:
            print "Error on data type. Please input Pandas Series"
        columns = ["value"]
        b = DataFrame(data.tolist(),index=data.index, columns=columns)
        return b
    def _is_anomaly_point(self):
        max_idx = self.index.max()
        max_anomaly_idx = self.anomaly_idx.max()
        if max_idx == max_anomaly_idx:
            print "Anomaly"
            produce = {
                "anomaly": 0
            }
            return DataFrame([produce], index=[to_datetime(max_anomaly_idx)])
        return None
