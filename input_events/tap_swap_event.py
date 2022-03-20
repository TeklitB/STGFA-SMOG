import random
import subprocess
import re

def get_screen_size():
    display_width = 1000
    display_height = 100

    process = subprocess.Popen('adb shell wm size', 
    stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, errout = process.communicate()
    display_area = re.search(r'(\d+)x(\d+)', output.decode())
    #print("Screen size is: ", display_area)

    if display_area:
        display_width = int(display_area.group(1))
        display_height = int(display_area.group(2))
    
    return display_width, display_height

def get_display_area():
    display_width = 1000
    display_height = 1000

    process = subprocess.Popen('adb shell dumpsys window displays',
    stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, errout = process.communicate()

    disparea_str = output.decode()
    display_size = re.search(r'app=(\d+)x(\d+)', disparea_str)
    
    if display_size:
        display_width = int(display_size.group(1))
        display_height = int(display_size.group(2))
    
    return display_width, display_height
# x              y
#display_width, display_height = get_screen_size()

def get_tap_coordinates():
    display_width, display_height = get_display_area()
    return 'tap {0} {1}'.format(random.randrange(display_width), random.randrange(display_height))

def gen_swipe_coordinates():
    display_width, display_height = get_display_area()
    return 'swipe {0} {1} {2} {3}'.format(random.randrange(display_width), random.randrange(display_height), random.randrange(display_width), random.randrange(display_height))

def gen_draganddrop_coordinates():
    display_width, display_height = get_display_area()
    return 'draganddrop {0} {1} {2} {3}'.format(random.randrange(display_width), random.randrange(display_height), random.randrange(display_width), random.randrange(display_height))

if __name__ == "__main__":
    #print(get_tap_coordinates())
    #print(gen_swipe_coordinates())
    print(get_display_area())