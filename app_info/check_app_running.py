import subprocess as sub
import time

def app_crashed(packagename):
    pro_pid = sub.Popen("adb shell pidof {0}".format(packagename), 
        stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
    out_pid, err_pid = pro_pid.communicate()
    
    # Restart app if it does not have process id (PID)
    if out_pid == "":
        # Restart app
        proc_start = sub.Popen('adb shell monkey -p '+ packagename +' -c android.intent.category.LAUNCHER 1',
        stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
        stdoutdata_start, stderrdata_start = proc_start.communicate()
        time.sleep(5)

