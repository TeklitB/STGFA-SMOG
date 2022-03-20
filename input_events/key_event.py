import random

# Key events that perform system operations
# ARRAY_OF_KEYEVENTS = [ "KEYCODE_HOME", "KEYCODE_BACK",
#                     "KEYCODE_CALL", "KEYCODE_ENDCALL",
#                     "KEYCODE_VOLUME_UP", "KEYCODE_VOLUME_DOWN",
#                     "KEYCODE_VOLUME_MUTE", "KEYCODE_MUTE",
#                     "KEYCODE_BRIGHTNESS_UP", "KEYCODE_BRIGHTNESS_DOWN",
#                     "KEYCODE_DPAD_UP", "KEYCODE_DPAD_DOWN",
#                     "KEYCODE_DPAD_LEFT", "KEYCODE_DPAD_RIGHT"
#                 ]

# Key events that perform system operations
SYSTEM_KEYEVENTS = [ "KEYCODE_HOME", "KEYCODE_BACK",
                     "KEYCODE_CALL", "KEYCODE_ENDCALL",
                     "KEYCODE_VOLUME_UP", "KEYCODE_VOLUME_DOWN",
                     "KEYCODE_VOLUME_MUTE", "KEYCODE_MUTE"
                 ]
#Major navigation keyevents. Such events should not be sent much 
MAJOR_NAV_KEYEVENTS = ["KEYCODE_MENU", "KEYCODE_SOFT_RIGHT", "KEYCODE_DPAD_CENTER"]

# Navigation Keyevents that move around the UI
NAV_KEYEVENTS = ["KEYCODE_DPAD_UP", "KEYCODE_DPAD_DOWN", "KEYCODE_DPAD_LEFT", "KEYCODE_DPAD_RIGHT"]

def generate_keyevent():
    keychoice = random.random()
    if keychoice < 0.1:
        return 'keyevent {}'.format(MAJOR_NAV_KEYEVENTS[random.randrange(len(MAJOR_NAV_KEYEVENTS))])
    elif keychoice < 0.3:
        return 'keyevent {}'.format(SYSTEM_KEYEVENTS[random.randrange(len(SYSTEM_KEYEVENTS))])
    else:
        longpres = random.random()
        if longpres < 0.3:
            return 'keyevent --longpress {}'.format(NAV_KEYEVENTS[random.randrange(len(NAV_KEYEVENTS))])
        else:
            return 'keyevent {}'.format(NAV_KEYEVENTS[random.randrange(len(NAV_KEYEVENTS))])