import subprocess

def local_cmd(command):
    #print('Sending command: {}'.format(command))
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdoutdata, stderrdata = proc.communicate()
    return stdoutdata #command

def adb_cmd(command):
    return local_cmd('adb {}'.format(command))

def adb_shell_cmd(command):
    return adb_cmd('shell {}'.format(command))

def adb_shell_input_cmd(command):
    return adb_shell_cmd('input {}'.format(command))

def install_app(app_path):
    adb_cmd('install {}'.format(app_path))

def uninstall_app(package_name):
    adb_cmd('uninstall {}'.format(package_name))