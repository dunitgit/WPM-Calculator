#!/usr/bin/env python

"""
Words per minute calculator.
"""

import sys
import time
import tty
import termios
import wikipedia
from termcolor import colored


def restart_line():
    """ Overwrite current line """
    sys.stdout.write('\r')
    sys.stdout.flush()


def print_wpm(count, start, end):
    """ Print WPM """
    if end - start != 0:
        print('Word count: ' + str(count))
        print('WPM: ' + str(int(round((count / (end - start)) * 60))))


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


def run(text):
    """ Run the WPM calculator """
    # text length
    text_len = len(text)
    # word count
    word_count = len(text.split(' '))
    # Progress counter
    char_counter = 0
    # First char hit flag
    first_char = True
    # Terminate flag
    terminate = False
    # Start case
    sys.stdout.write(colored(text[char_counter], 'blue') + text[1:])
    restart_line()

    for text_char in text:
        while not terminate:
            key_press = getch()
            # User terminated program
            if key_press == 'å':
                terminate = True
            # User hit the correct key
            if key_press == text_char:
                if first_char:
                    # Start counting seconds when the user hit the first char
                    start_time = time.time()
                    first_char = False
                if char_counter == text_len - 1:
                    # Stop counting seconds when the user hit the last char
                    end_time = time.time()
                    print(colored(text, 'green'))
                    terminate = True
                    break
                # Update char counter and visual progress
                char_counter += 1
                sys.stdout.write(colored(text[0:char_counter], 'green') +
                                 colored(text[char_counter], 'blue') +
                                 text[char_counter + 1: text_len])
                restart_line()
                break

    # If the user did not complete dont print summary
    if end_time != 0:
        print_wpm(word_count, start_time, end_time)


def get_text(max_tries, count):
    """ Get text challenge """
    if count > max_tries:
        print("Something went wrong. Using fallback text")
        return 'Fallback text here yoyoy'
    # Get a random wiki page
    random = wikipedia.random(1)
    try:
        # Get summary of page
        page = wikipedia.page(random).summary
    except wikipedia.exceptions.DisambiguationError:
        page = get_text(max_tries, count + 1)
    splitted = page.split(' ')
    result = ''
    # Atm we strip the summary to 10 words, as we cannot handle multi
    # line reset (this also means we make the nasty assumption that 10 words can fit
    # in one line in the terminal)
    for i in range(0, 10):
        try:
            result += splitted[i]
        # Summary is less than 10 words. Return the result
        except IndexError:
            return result
        if i < 9:
            result += ' '
    return result

run(get_text(3, 0))
