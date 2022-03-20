import random

#ARRAY_OF_TEXTS = ["admin", "hellow%sworld", "password", "Android%stesting"] %s

def generate_text_input():
    random_text_input = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789') for x in range(random.randint(5, 10)))
    return 'text {}'.format(random_text_input)