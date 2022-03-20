import subprocess
import time
import settings
import subprocess as sub

#Pixel_XL_API_28
#emulator -avd api28_0 -wipe-data -no-audio -no-window
def boot_devices():
	"""
	prepare the env of the device
	:return:
	"""
	for i in range(0, settings.DEVICE_NUM):
		device_name = settings.AVD_SERIES + str(i)
		print("Booting Device:", device_name)
		time.sleep(0.3)
		if settings.HEADLESS:
			sub.Popen('emulator -avd ' + device_name + " -wipe-data -no-audio -no-window",
					  stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
		else:
			sub.Popen('emulator -avd ' + device_name + " -wipe-data -no-audio",
					  stdout=sub.PIPE, stderr=sub.PIPE, shell=True)

	print("Waiting", settings.AVD_BOOT_DELAY, "seconds")
	time.sleep(settings.AVD_BOOT_DELAY)

if __name__ == "__main__":
    boot_devices()