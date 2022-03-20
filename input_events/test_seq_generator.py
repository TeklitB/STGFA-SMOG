import random
from input_events import key_event, get_events
from input_events import text_event
from input_events import tap_swap_event
from input_events import action_commands
import settings
from deap import creator

def gen_test_seq():
    test_seq = []
    test_seq_len = random.randrange(settings.SEQUENCE_LENGTH_MIN, settings.SEQUENCE_LENGTH_MAX)

    i=0
    for i in range(test_seq_len):
        action = action_commands.select_action()
        test_seq.append(get_events.get_events_by_actiontype(action))
    
    return creator.Individual(test_seq)