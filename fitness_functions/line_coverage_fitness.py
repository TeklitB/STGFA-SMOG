from fitness_functions.fitnessbase import FitnessFunctions
from fitness_functions.extract_coverage import extract_code_coverage
import settings

class LineCoverage(FitnessFunctions):
    def __init__(self, packagename, individual, index_indv, gen):
        self.packagename = packagename
        self.individual = individual
        self.index_indv = index_indv
        self.gen = gen
    
    def getFitness_value(self):
        return extract_code_coverage(self.packagename)[0]

if __name__ == "__main__":
    pathto = settings.ACVTOOL_WDIR+"report/org.scoutant.blokish/report/index.html"
    lin = LineCoverage()
    print(lin.getFitness_value())