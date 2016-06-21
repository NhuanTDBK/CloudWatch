from outlier.BaseOutlier import BaseOutlier
from sklearn.svm import OneClassSVM
import numpy as np
class OneClassSVM(BaseOutlier):
    def __init__(self,nu=0.1,kernel='rbf',gamma=0.1):
        self.nu = nu
        self.kernel = kernel
        self.gamma = gamma
    def fit(self,data=None):
        self.check_finite(data)
        if(self._is_using_pandas(data)==True):
            self.data.interpolate(inplace=True)
        self.data = data.reshape(-1,1)
        self.clf = OneClassSVM(nu=self.nu, kernel=self.kernel, gamma=self.gamma)
        self.clf.fit(data)
        return self
    def predict(self, X_test):
        return self.clf.predict(X_test)

