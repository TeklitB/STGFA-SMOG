import abc

class FitnessFunctions(object):
    __metaclass__ = abc.ABCMeta
    @abc.abstractmethod
    def getFitness_value(self):
        pass
