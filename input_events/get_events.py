from input_events import key_event, text_event, tap_swap_event
import random

def get_events_by_actiontype(action):
    percent = random.random()
    if action == "keyevent":
        return key_event.generate_keyevent()
    elif action == "text":
        return text_event.generate_text_input()
    elif action == "tap":
        return tap_swap_event.get_tap_coordinates()
    elif action == "swipe":
        return tap_swap_event.gen_swipe_coordinates()
    elif action == "draganddrop":
        return tap_swap_event.gen_draganddrop_coordinates()