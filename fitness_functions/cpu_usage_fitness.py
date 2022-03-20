import subprocess, os, glob

from fitness_functions.fitnessbase import FitnessFunctions


class CpuUsage(FitnessFunctions):
    def __init__(self, packagename, index_indv, gen):
        self.packagename = packagename
        self.index_indv = index_indv
        self.gen = gen
    
    def getFitness_value(self):
        total_cpu = 0

        # Check if a file exists
        if len(os.listdir('cpu_usage_stats/') ) != 0:
            files = glob.glob('cpu_usage_stats/*')
            for f in files:
                os.remove(f)
        
        # First get PID of the application
        pro_pid = subprocess.Popen("adb shell pidof {0}".format(self.packagename), 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out_pid, err_pid = pro_pid.communicate()
        if out_pid.decode() == None:
            return total_cpu
        # Strip the trailing newline before using the PID output in the next command
        app_pid = out_pid.decode().rstrip("\n")

        # Getting CPU usage of the app with refresh time only onse
        proc = subprocess.Popen("adb shell top -p {0} -n 1".format(app_pid), 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        cpu_info, cpu_err = proc.communicate()

        # Write memory usage data to file
        #cpu_file_path = "cpu_usage_stats/cpu_data_"+str(self.gen)+str(self.index_indv)+".txt"
        #check_path = os.path.exists(cpu_file_path)
        #open_cpu_file = open(cpu_file_path, "a" if check_path else "w+")
        #open_cpu_file.write(cpu_info.decode())

        # Filter cpu usage from cpu info provided
        for line in cpu_info.decode().splitlines():
                if "user" in line:
                    items = line.split(" ")
                    for item in items:
                        if "user" in item:
                            parts = item.split("%")
                            return int(parts[0])
        #print("CPU: ", total_cpu)
        return total_cpu