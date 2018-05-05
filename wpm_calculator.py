"""
Words per minute calculator.
"""

import curses
from curses import wrapper
import time
import wikipedia

def main(stdscr):
    """ Program entry point """
    stdscr = curses.initscr() # create a window object that represents the terminal window
    curses.noecho() # Don't print what I type on the terminal
    curses.cbreak() # React to every key press, not just when pressing "enter"
    stdscr.keypad(True) # Enable easy key codes (will come back to this)
    curses.curs_set(0) # Curser get outta here!
    run(stdscr, get_text(3, 0))

def print_wpm(stdscr, count, start, end):
    """ Print WPM """
    if end - start != 0:
        stdscr.addstr('Word count: ' + str(count) + '\n')
        stdscr.addstr('WPM: ' + str(int(round((count / (end - start)) * 60))))
        stdscr.getch()

def run(stdscr, text):
    """ Run the WPM calculator """
    text_len = len(text) # text length
    word_count = len(text.split(' ')) # word count
    char_counter = 0 # Progress counter
    first_char = True # First char hit flag
    terminate = False # Terminate flag

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)

    stdscr.addstr(text[char_counter], curses.color_pair(1))
    stdscr.addstr(text[1:])

    for text_char in text:
        while not terminate:
            key_press = stdscr.getkey()
            if key_press == 'å': # User terminated program
                terminate = True
            if key_press == text_char: # User hit the correct key
                if first_char: # Start counting when the user hit the first char
                    start_time = time.time()
                    first_char = False
                if char_counter == text_len - 1: # Stop counting when the user hit the last char
                    end_time = time.time()
                    terminate = True
                    break
                char_counter += 1 # Update char counter and visual progress
                stdscr.clear()
                stdscr.addstr(text[0:char_counter], curses.color_pair(2))
                stdscr.addstr(text[char_counter], curses.color_pair(1))
                stdscr.addstr(text[char_counter + 1: text_len])
                break

    # If the user did not complete dont print summary
    if end_time != 0:
        stdscr.clear()
        print_wpm(stdscr, word_count, start_time, end_time)


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
    return page

wrapper(main)
