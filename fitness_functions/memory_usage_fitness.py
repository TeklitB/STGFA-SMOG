import os
import subprocess
import re

from fitness_functions.fitnessbase import FitnessFunctions

class MemoryUsage(FitnessFunctions):
    def __init__(self, packagename, index_indv, gen):
        self.packagename = packagename
        self.index_indv = index_indv
        self.gen = gen
    
    def getFitness_value(self):
        total_memory = 0
        proc = subprocess.Popen("adb shell dumpsys meminfo {}".format(self.packagename), 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        memoryInfo, errInfo = proc.communicate()

        # Write memory usage data to file
        #mem_file_path = "mem_usage_stats/mem_data_"+str(self.gen)+str(self.index_indv)+".txt"
        #check_path = os.path.exists(mem_file_path)
        #open_mem_file = open(mem_file_path, "a" if check_path else "w+")
        #open_mem_file.write(memoryInfo.decode())
        
        for line in memoryInfo.decode().splitlines():
            find_mem = re.search(r"(\s+)(TOTAL)(\s+)(\d+)", line)
            if find_mem:
                total_memory = int(find_mem.group(4))
                break
            else:
                continue
        
        return total_memory