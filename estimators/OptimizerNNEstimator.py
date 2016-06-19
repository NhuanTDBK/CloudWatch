from sklearn.base import BaseEstimator

class OptimizerNNEstimator(BaseEstimator):
    def __init__(self,optimizer=None,model_fn=None):
        self.optimizer = optimizer
        self.model_fn = model_fn
    def fit(self,X,y,**fit_params):
        if(self.optimizer==None):
            self.model_fn.fit(X,y)
            return self
        if(isinstance(fit_params,dict)&fit_params.has_key('neural_shape')):
            self.neuron_shape = fit_params.get("neural_shape")
            self.optimizer.fit(X,y,**fit_params)
        else:
            self.optimizer.fit(X,y)
        fit_params["weights_matrix"] = self.optimizer.best_archive
        self.model_fn.fit(X,y,**fit_params)
        return self
    def predict(self,X):
        return self.model_fn.predict(X)
    def score(self,X,y):
        return self.model_fn.score(X,y)
    def save(self,fname):
        return self.model_fn.save(fname)
