from fitness_functions.fitnessbase import FitnessFunctions
from fitness_functions.extract_coverage import extract_code_coverage

class ClassCoverage(FitnessFunctions):
    def __init__(self, packagename, individual, index_indv, gen):
        self.packagename = packagename
        self.individual = individual
        self.index_indv = index_indv
        self.gen = gen
    
    def getFitness_value(self):
        return extract_code_coverage(self.packagename)[2]

if __name__ == "__main__":
    pathto = "/home/tbg/acvtool/acvtool_working_dir/report/org.scoutant.blokish/report/index.html"
    cla = ClassCoverage()
    print(cla.getFitness_value())