import sys
import subprocess
import re
import os

from fitness_functions.fitnessbase import FitnessFunctions

class Crashes(FitnessFunctions):
    def __init__(self, packagename, individual, index_indv, gen):
        self.packagename = packagename
        self.individual = individual
        self.index_indv = index_indv
        self.gen = gen
    
    def getFitness_value(self):
        # Search for AndroidRuntime Fatal Exception to count number of crashes
        catched_runtime = 'E AndroidRuntime: FATAL EXCEPTION: main\n'

        unique_crahes = set()
    
        # File to store the original crashes retrieved from logcat
        
        Logcat_CMD = "adb logcat -d -b crash AndroidRuntime:E *:S"

        # Log crashes from the Logcat for each individual
        process = subprocess.Popen(Logcat_CMD, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        proc_out, proc_err = process.communicate()
        #print(proc_out)

        if proc_out != "":
            original_crash = "crash_logs/crash_logcat_timestamp_"+str(self.gen)+str(self.index_indv)+".txt"
            check_path_original = os.path.exists(original_crash)
            open_original = open(original_crash, "a" if check_path_original else "w+")
            open_original.write(str(proc_out))
            open_original.close()

            # File used to store crashes filtered for timestamp, and PID
            filtered_crash = "crash_logs/crash_logs_"+str(self.gen)+str(self.index_indv)+".txt"

            #os.makedirs(os.path.dirname(filtered_crash), exist_ok=True)
            check_path_filtered = os.path.exists(filtered_crash)
            filtered_crash_open = open(filtered_crash, "a" if check_path_filtered else "w+")

            with open(original_crash, 'r') as reader:
                # Read and print the entire file line by line
                line = reader.readline()
                while line != '':  # The EOF char is an empty string
                    line = re.sub(r'\d+-\d+\s+\d+:\d+:\d+.\d+\s+\d+\s+\d+\s+', '', line)
                    line = re.sub(r'\s+PID:\s+\d+', '', line)
                    filtered_crash_open.write(line)
                    line = reader.readline()
            
            filtered_crash_open.close()

            with open(filtered_crash, 'r') as readerit:
                # Read the entire file line by line
                line = readerit.readline()
                #print(line)
                one_crash = ''
                while line != '':  # The EOF char is an empty string
                    one_crash = one_crash + line
                    line = readerit.readline()
                    if str(line)==catched_runtime:
                        if self.packagename in one_crash and catched_runtime in one_crash:
                            unique_crahes.add(one_crash)
                        one_crash = ''
                    if line == '':
                        if self.packagename in one_crash and catched_runtime in one_crash:
                            unique_crahes.add(one_crash)
            
            #for un_crash in unique_crahes:
                #print(un_crash)
            # Log the test case that triggered the crash
            if len(unique_crahes) > 0:
                crash_testcase = "crash_logs/crash_testcase_"+str(self.gen)+str(self.index_indv)+".txt"
                check_path_test = os.path.exists(crash_testcase)
                open_crashtest = open(crash_testcase, "a" if check_path_test else "w+")
                open_crashtest.write(str(self.individual))
                print("Crash found: {}".format(len(unique_crahes)))
        
        return len(unique_crahes)



