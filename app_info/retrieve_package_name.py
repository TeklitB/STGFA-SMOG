import os
import subprocess

def get_package_name(path):
	apk_path = None
	if path.endswith(".apk"):
		apk_path = path
	else:
		for file_name in os.listdir(path + "/bin"):
			if file_name == "bugroid-instrumented.apk":
				apk_path = path + "/bin/bugroid-instrumented.apk"
				break
			elif file_name.endswith("-debug.apk"):
				apk_path = path + "/bin/" + file_name

	assert apk_path is not None

	get_package_cmd = "aapt d xmltree " + apk_path + " AndroidManifest.xml | grep package= | awk 'BEGIN {FS=\"\\\"\"}{print $2}'"
	# print get_package_cmd
	package_name = subprocess.Popen(get_package_cmd, shell=True, stdout=subprocess.PIPE).communicate()[0].strip()
	return package_name, apk_path