import subprocess
import time

from runtests.runtestcases import run_test_case

# Set the application under test before running
def setup_aut(individual, package_name, index_indv, gen, app_name):
    #  Clear logcat before running new test cases
    proc_log = subprocess.Popen("adb shell logcat -b all -c", 
    stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    clear_out, clear_err = proc_log.communicate()
    print(clear_out.decode())
    
    # Forcefully stop the app
    proc_am = subprocess.Popen("adb shell am force-stop " + package_name,
     stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdoutdata_am, stderrdata_am = proc_am.communicate()

    # Clean the states of the app
    proc_pm = subprocess.Popen("adb shell pm clear " + package_name,
     stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdoutdata_pm, stderrdata_pm = proc_pm.communicate()

    # Reset battery data gathered
    proc_batt = subprocess.Popen("adb shell dumpsys batterystats --reset", shell=True)
    stdoutdata_batt, stderrdata_batt = proc_batt.communicate()

    # Restart app
    proc_start = subprocess.Popen('adb shell monkey -p '+ package_name +' -c android.intent.category.LAUNCHER 1',
    stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdoutdata_start, stderrdata_start = proc_start.communicate()
    print("Waiting for application to start!...")
    time.sleep(5)
    print("Application started!")

    fitness_values = run_test_case(individual, package_name, index_indv, gen, app_name)

    return fitness_values