from outlier.BaseOutlier import BaseOutlier
from sklearn.svm import OneClassSVM
import pandas as pd
import numpy as np
class OneClassSVMDetector(BaseOutlier):
    @staticmethod
    def get_attributes():
        return {
            "nu":0.1,
            "kernel":['rbf','linear', 'poly', 'rbf', 'sigmoid', 'precomputed'],
            "gamma":0.1,
        }
    def __init__(self,nu=0.1,kernel='rbf',gamma=0.1):
        self.nu = nu
        self.kernel = kernel
        self.gamma = gamma
    def fit(self,data=None):
        self.data = data
        self.check_finite(data)
        if(self._is_using_pandas(data)==True):
            self.data.interpolate(inplace=True)
        # self.datareshap = data.reshape(-1,1)
        self.clf = OneClassSVM(nu=self.nu, kernel=self.kernel, gamma=self.gamma)
        self.clf.fit(data.reshape(-1,1))
        # print "done"
        return self
    def predict(self, X_test):
        y_pred_train = self.clf.predict(X_test.reshape(-1,1))

        outlier_idx = np.where(y_pred_train == -1)
        inlier_idx = np.where(y_pred_train == 1)
        d = {
            'timestamp': self.data.index[outlier_idx],
            'anoms': self.data.iloc[outlier_idx]
        }
        anoms = pd.DataFrame(d)
        self.anomaly_idx = anoms.index
        self.anom_val = anoms['anoms']
        return anoms
    def fit_predict(self, data=None):
        self.fit(data)
        return self.predict(data)
    def plot(self):
        import matplotlib.pyplot as plt
        f, ax = plt.subplots(1, 1)
        ax.plot(self.data, 'b')
        ax.plot(self.anomaly_idx, self.anom_val, 'ro')
        ax.set_title('Detected Anomalies')
        ax.set_ylabel('Count')
        f.tight_layout()
        return f
