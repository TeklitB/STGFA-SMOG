import os, re, glob
import subprocess
from fitness_functions.fitnessbase import FitnessFunctions

class NetworkUsage(FitnessFunctions):
    def __init__(self, packagename, individual, index_indv, gen):
        self.packagename = packagename
        self.individual = individual
        self.index_indv = index_indv
        self.gen = gen
    
    def getFitness_value(self):

        total_netusage = 0

        # Check if a file exists
        if len(os.listdir('net_usage/') ) != 0:
            files = glob.glob('net_usage/*')
            for f in files:
                os.remove(f)
        
        # Create file to log network usage
        net_stats = "net_usage/netusage_"+str(self.gen)+str(self.index_indv)+".txt"

        # Log network usage for each test case
        NETUSAGE_CMD = "adb shell cat /proc/net/xt_qtaguid/stats > "+net_stats
        netusageProc = subprocess.Popen(NETUSAGE_CMD, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        netusage_out, netusage_err = netusageProc.communicate()

        # Find UID of the app
        UID_CMD = "adb shell dumpsys package "+self.packagename+" | grep userId"
        findUID = subprocess.Popen(UID_CMD, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        uid_out, uid_err = findUID.communicate()
        app_uid = uid_out.decode("utf-8").split("=")[1]
        app_uid_trim = str(app_uid).strip("\n")
        #print(str(app_uid_trim)+" 0")

        with open(net_stats, 'r') as reader:
            # Read and print the entire file line by line
            line = reader.readline()
            while line != '':  # The EOF char is an empty string
                # Find background network usage
                if re.search(app_uid_trim+" 0", str(line)):
                    rxb_bg_netusage = str(line).split(" ")[5]
                    txb_bg_netusage = str(line).split(" ")[7]
                    total_netusage = total_netusage + int(rxb_bg_netusage) + int(txb_bg_netusage)
                # Find foreground network usage
                if re.search(app_uid_trim+" 1", str(line)):
                    rxb_fg_netusage = str(line).split(" ")[5]
                    txb_fg_netusage = str(line).split(" ")[7]
                    total_netusage = total_netusage + int(rxb_fg_netusage) + int(txb_fg_netusage)
                    break
                line = reader.readline()
        
        return total_netusage

if __name__ == "__main__":
    netf = NetworkUsage()
    print(netf.getFitness_value())