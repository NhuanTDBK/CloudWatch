import numpy as np
class TrainObject:
    def __init__(self,X_train=None,y_train=None,X_test=None,y_test=None,metadata=None):
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        self.metadata = metadata
    def __repr__(self):
        output = "Metadata of train object: %s"%self.metadata
        return output
    def getitems(self):
        return self.X_train,self.y_train,self.X_test,self.y_test