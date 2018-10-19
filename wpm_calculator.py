#!/usr/bin/python3

"""
Words per minute calculator.
"""

import curses
import time
import requests
import sys


def main(stdscr):
    """ Program entry point """
    # Check for user text
    if len(sys.argv) == 1:
        text_is_provided = False
    elif len(sys.argv) == 2:
        text_is_provided = True
    else:
        sys.exit("Error: too many parameters provided")
    # Don't print what is typed in the terminal
    curses.noecho()
    # React to every key press, not just when pressing 'Enter'
    curses.cbreak()
    # Enable easy key codes
    stdscr.keypad(True)
    # Remove cursor
    curses.curs_set(0)
    # Clear screen
    stdscr.clear()
    # Refresh screen
    stdscr.refresh()
    # Init colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)
    # Initial user input (get next text)
    key = 266

    # Run until user press 'ESC'
    while key != 27:
        # Clear screen
        stdscr.clear()
        # Check for specific user inputs
        # F1 (Restart)
        if key == 265:
            char_counter = 0
            first_char = True
            start_time = 0
            end_time = 0
            mistypes = 0
        # F2 (New text)
        if key == 266:
            if (text_is_provided):
                filepath = sys.argv[1]
                try:
                    text_file = open(filepath, 'r')
                    text = text_file.read()
                except IOError:
                    sys.exit("Error: could not read file: " + filepath)
            else:
                text = get_random_text()
            text_len = len(text)
            word_count = len(text.split(' '))
            char_counter = 0
            first_char = True
            start_time = 0
            end_time = 0
            mistypes = 0
        # User hit the correct key
        if key == ord(text[char_counter]):
            # Start timer when the user hit the first character
            if first_char:
                start_time = time.time()
                first_char = False
            # Check if done
            if char_counter == text_len - 1:
                end_time = time.time()
                stdscr.clear()
                key = render_scorescreen(
                    stdscr, word_count, start_time, end_time, mistypes)
                # If restart was not pressed we serve a new text
                if key != 27:
                    key = 266
                continue
            # Update character counter
            char_counter += 1
        # User didnt hit correct key
        elif key not in (265, 266) and not first_char:
            mistypes += 1
        render_text(stdscr, text, text_len, char_counter)
        render_bottom_menu(stdscr, mistypes)

        stdscr.refresh()
        key = stdscr.getch()


def render_text(stdscr, text, text_len, char_counter):
    """ Render text """
    stdscr.addstr(text[0:char_counter], curses.color_pair(2))
    stdscr.addstr(text[char_counter], curses.color_pair(1))
    stdscr.addstr(text[char_counter + 1: text_len])


def render_bottom_menu(stdscr, mistypes):
    """ Render bottom menu """
    bottom_menu = "Restart: 'F1' | New text: 'F2' | Quit: 'ESC'"
    error_count = "Errors: " + str(mistypes)
    height, width = stdscr.getmaxyx()
    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(height - 1, 0, bottom_menu)
    stdscr.addstr(height - 1, len(bottom_menu), " " *
                  (width - len(bottom_menu) - 1))
    stdscr.addstr(height - 1, width - (len(error_count) + 1), error_count)
    # Workaround to be able to color the lower right field
    stdscr.insch(height - 1, width - 1, " ")
    stdscr.attroff(curses.color_pair(3))


def render_scorescreen(stdscr, count, start, end, mistypes):
    """ Render scorescreen """
    stdscr.addstr('Words: ' + str(count) + '\n')
    stdscr.addstr('Errors: ' + str(mistypes) + '\n')
    stdscr.addstr('Time: ' + str(round(end - start)) + ' seconds\n')
    stdscr.addstr(
        'WPM: ' + str(int(round((count / (end - start)) * 60))) + '\n')
    stdscr.addstr(
        'Accuracy: ' + str(round(100 - (mistypes / count) * 100)) + '%\n\n')
    stdscr.addstr('Press any key to play again...' + '\n')
    render_bottom_menu(stdscr, mistypes)
    return stdscr.getch()


def get_random_text():
    """ Get random text from wikipedia"""
    # Get a random wiki page
    random_page = requests.get('https://en.wikipedia.org/w/api.php?'
                               'format=json'
                               '&action=query'
                               '&list=random'
                               '&rnlimit=1'
                               '&rnnamespace=0')
    random_page_id = str(random_page.json()['query']['random'][0]['id'])
    page = requests.get('https://en.wikipedia.org/w/api.php?'
                        'format=json'
                        '&action=query'
                        '&prop=extracts'
                        '&exintro'
                        '&explaintext'
                        '&redirects=1'
                        '&pageids=' + random_page_id)
    page_summary = page.json()['query']['pages'][random_page_id]['extract']
    return page_summary.rstrip().replace('\n', ' ').replace('\r', ' ')


curses.wrapper(main)
