import os, re, glob
import subprocess
from fitness_functions.fitnessbase import FitnessFunctions

class BatteryUsage(FitnessFunctions):
    def __init__(self, packagename, individual, index_indv, gen):
        self.packagename = packagename
        self.individual = individual
        self.index_indv = index_indv
        self.gen = gen
    
    def getFitness_value(self):
        total_battusage = 0.0
        app_uid = None

        # Check if a file exists
        if len(os.listdir('batt_usage/') ) != 0:
            files = glob.glob('batt_usage/*')
            for f in files:
                os.remove(f)
        
        # Create file to log battery usage
        batt_stats = "batt_usage/battusage_"+str(self.gen)+str(self.index_indv)+".txt"

        # Log network usage for each test case
        BATTUSAGE_CMD = "adb shell dumpsys batterystats > "+self.packagename+" > "+batt_stats
        battusageProc = subprocess.Popen(BATTUSAGE_CMD, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        battusage_out, battusage_err = battusageProc.communicate()

        with open(batt_stats, 'r') as reader:
            # Read and print the entire file line by line
            line = reader.readline()
            while line != '':  # The EOF char is an empty string
                # Search the line containing the UID of the app
                line_withUID = re.search(r'top=\w+:\"'+self.packagename+"\"", line) # +top=u0a85:"org.uaraven.e"
                
                # Filter the UID of the app
                if line_withUID:
                    line_uid = line.split("=")[1]
                    app_uid = line_uid.split(":")[0]
                    break
                line = reader.readline()
        
        # If UID of the app is found filter its power use
        if app_uid != None:
            with open(batt_stats, 'r') as reader:
                # Read and print the entire file line by line
                line = reader.readline()
                while line != '':  # The EOF char is an empty string Uid u0a85:
                    # Find the line containing power use of the app
                    line_withbattuse = re.search(r"Uid +"+app_uid+":", line)
                    
                    # Filter the power use of the app
                    if line_withbattuse:
                        battuse_line = line.split(":")[1]
                        total_battusage = float(battuse_line.split(" ")[1])
                        break
                    line = reader.readline()
        
        return total_battusage
        #return app_uid

if __name__ == "__main__":
    battf = BatteryUsage()
    print(battf.getFitness_value())