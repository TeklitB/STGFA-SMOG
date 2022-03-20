import subprocess
import os, shutil
import time
from app_info.check_app_running import app_crashed
import settings

def acvtool(app_name, packagename, individual):
    # Delete existing report generated folder
    report_fold = settings.ACVTOOL_WDIR+"report/"
    if os.path.exists(report_fold):
        shutil.rmtree(report_fold, ignore_errors=False, onerror=None)

    print("Starting code coverage...")   
    # Start the acvtool
    start_app = subprocess.Popen("acv start {0}".format(packagename), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    time.sleep(5)

    # Restart app
    proc_start = subprocess.Popen('adb shell monkey -p '+ packagename +' -c android.intent.category.LAUNCHER 1', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    proc_start_out, proc_start_err = proc_start.communicate()
    print("Waiting for application to start...")
    time.sleep(5)
    print("Application started!")

    # Here run the test cases
    print("Test cases running separately for code coverage")
    for line in individual:
        #app_crashed(packagename)
        proc_test = subprocess.Popen("adb shell input "+line,
         stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        proc_test_out, proc_test_err = proc_test.communicate()
    
    # Stop acvtool after all test cases are executed
    stop_app = subprocess.Popen("acv stop {0}".format(packagename), shell=True)
    time.sleep(10)

    print("Starter process Killed: {0}".format(start_app.poll()))
    # Generate code coverage report
    REPORT_CMD = "acv report "+ packagename +" -p "+settings.ACVTOOL_CMDDIR+"metadata/"+app_name+".pickle"
    repo_proc = subprocess.Popen(REPORT_CMD, shell=True)
    repo_out, repo_err = repo_proc.communicate()

