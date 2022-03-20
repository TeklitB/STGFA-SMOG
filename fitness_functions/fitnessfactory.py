
from fitness_functions.line_coverage_fitness import LineCoverage
from fitness_functions.crash_fitness import Crashes
from fitness_functions.cpu_usage_fitness import CpuUsage
from fitness_functions.memory_usage_fitness import MemoryUsage
from fitness_functions.testcase_length_fitness import TestcaseLength
from fitness_functions.network_usage_fitness import NetworkUsage
from fitness_functions.battery_usage_fitness import BatteryUsage
from fitness_functions.line_coverage_fitness import LineCoverage
from fitness_functions.method_coverage_fitness import MethodCoverage
from fitness_functions.class_coverage_fitness import ClassCoverage
import settings

class FitnessFunctionFactory:
    def __init__(self, individual, packagename, index_indv, gen):
        #self.script_file = script_file
        self.individual = individual
        self.packagename = packagename
        self.index_indv = index_indv
        self.gen = gen
    
    def get_fintess_functions(self, fitnessnames):
        selected_fitness = []
                
        for fitname in fitnessnames:
            # Crash fitness function
            if fitname == settings.CRASH:
                selected_fitness.append(Crashes(self.packagename, self.individual, self.index_indv, self.gen))
            
            # Test case length fitness function
            if fitname == settings.LENGTH:
                selected_fitness.append(TestcaseLength(self.individual, self.packagename, self.index_indv, self.gen))
            
            # App usage fitness functions
            if fitname == settings.CPU:
                selected_fitness.append(CpuUsage(self.packagename, self.index_indv, self.gen))
            if fitname == settings.MEMORY:
                selected_fitness.append(MemoryUsage(self.packagename, self.index_indv, self.gen))
            if fitname == settings.NETWORK:
                selected_fitness.append(NetworkUsage(self.packagename, self.individual, self.index_indv, self.gen))
            if fitname == settings.BATTERY:
                selected_fitness.append(BatteryUsage(self.packagename, self.individual, self.index_indv, self.gen))
            
            # Code coverage fitness functions
            if fitname == settings.LINECOVERAGE:
                selected_fitness.append(LineCoverage(self.packagename, self.individual, self.index_indv, self.gen))
            if fitname == settings.METHODCOVERAGE:
                selected_fitness.append(MethodCoverage(self.packagename, self.individual, self.index_indv, self.gen))
            if fitname == settings.CLASSCOVERAGE:
                selected_fitness.append(ClassCoverage(self.packagename, self.individual, self.index_indv, self.gen))
        
        return selected_fitness

