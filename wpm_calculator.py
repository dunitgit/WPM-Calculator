#!/usr/bin/env python

"""
Words per minute calculator.
"""

import sys
import time
import tty
import termios
from termcolor import colored


def restart_line():
    """ Overwrite current line """
    sys.stdout.write('\r')
    sys.stdout.flush()


def print_wpm(count, start, end):
    """ Print WPM """
    if end - start != 0:
        print('Word count: ' + str(count))
        print('WPM: ' + str(int(round((WORD_COUNT / (end - start)) * 60))))


def getch():
    """ Get user key press """
    file_des = sys.stdin.fileno()
    old_settings = termios.tcgetattr(file_des)
    try:
        tty.setraw(sys.stdin.fileno())
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(file_des, termios.TCSADRAIN, old_settings)
    return key


# Text challenge
# todo: load from user input and/or web
TEXT = 'Greek is a land feature and reserve located 11 km south of Perth'

# Text length
TEXT_LEN = len(TEXT)

# Word count
WORD_COUNT = len(TEXT.split(' '))

# Time handling
start_time = 0
end_time = 0

# Progress counter
char_counter = 0

# First char hit flag
firstChar = True

# Terminate flag
terminate = False

# Get user input object
#getch = _GetchUnix()


# Start case
sys.stdout.write(colored(TEXT[char_counter], 'blue') + TEXT[1:])
restart_line()

for c in TEXT:
    while not terminate:
        key_press = getch()
        # User terminated program
        if key_press == '':
            terminate = True
        # User hit the correct key
        if key_press == c:
            if firstChar:
                # Start counting seconds when the user hit the first char
                start_time = time.time()
                firstChar = False
            if char_counter == TEXT_LEN - 1:
                # Stop counting seconds when the user hit the last char
                end_time = time.time()
                print(colored(TEXT, 'green'))
                terminate = True
                break
            # Update char counter and visual progress
            char_counter += 1
            sys.stdout.write(colored(TEXT[0:char_counter], 'green') +
                             colored(TEXT[char_counter], 'blue') +
                             TEXT[char_counter + 1: TEXT_LEN])
            restart_line()
            break

# If the user did not complete dont print summary
if end_time != 0:
    print_wpm(WORD_COUNT, start_time, end_time)
