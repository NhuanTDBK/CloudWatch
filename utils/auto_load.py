class AutoLoad(object):
    def load_engine(self, method):
        mod = __import__('outlier.%s' % method, fromlist=[method])
        klass = getattr(mod, method)
        return klass

    def auto_load_engine_default(self, method):
        object = self.load_engine(method)
        return object()


    def auto_load_engine_parameter(self, method):
        object = self.load_engine(method)
        return object.get_attributes()


    def auto_constructor(self, method, parameter):
        object = self.auto_load_engine_default(method)
        for item, value in parameter.iteritems():
            object.__setattr__(item, value)
        return object