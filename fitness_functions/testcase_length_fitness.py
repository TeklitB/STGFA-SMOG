
from fitness_functions.fitnessbase import FitnessFunctions


class TestcaseLength(FitnessFunctions):
    def __init__(self, individual, packagename, index_indv, gen):
        self.individual = individual
        self.packagename = packagename
        self.index_indv = index_indv
        self.gen = gen
    
    def getFitness_value(self):
        return(len(self.individual))