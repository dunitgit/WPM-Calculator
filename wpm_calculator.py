#!/usr/bin/python3

"""
Words per minute calculator.
"""

import curses
import time
import wikipedia

def main(stdscr):
    """ Program entry point """
    # Don't print what is typed in the terminal
    curses.noecho()
    # React to every key press, not just when pressing "enter"
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
    # Max number of attempts to fetch text from wikipedia
    wiki_max = 3
    # Initial user input (get next text)
    key = 266
    # Text variables
    text = ''
    text_len = 0
    word_count = 0
    char_counter = 0
    first_char = True

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
        # F2 (New text)
        if key == 266:
            text = get_text(wiki_max, 0)
            text_len = len(text)
            word_count = len(text.split(' '))
            char_counter = 0
            first_char = True
            start_time = 0
            end_time = 0

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
                key = render_scorescreen(stdscr, word_count, start_time, end_time)
                # If restart was not pressed we serve a new text
                if key != 265:
                    key = 266
                continue
            # Update character counter
            char_counter += 1

        render_text(stdscr, text, text_len, char_counter)
        render_bottom_menu(stdscr)

        stdscr.refresh()
        key = stdscr.getch()

def render_text(stdscr, text, text_len, char_counter):
    """ Render text """
    stdscr.addstr(text[0:char_counter], curses.color_pair(2))
    stdscr.addstr(text[char_counter], curses.color_pair(1))
    stdscr.addstr(text[char_counter + 1: text_len])

def render_bottom_menu(stdscr):
    """ Render bottom menu """
    bottom_menu = "Restart: 'F1' | New text: 'F2' | Quit: 'ESC'"
    height, width = stdscr.getmaxyx()
    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(height - 1, 0, bottom_menu)
    stdscr.addstr(height - 1, len(bottom_menu), " " * (width - len(bottom_menu) - 1))
    # Workaround to be able to color the lower right field
    stdscr.insch(height - 1, width - 1, " ")
    stdscr.attroff(curses.color_pair(3))

def render_scorescreen(stdscr, count, start, end):
    """ Render scorescreen """
    stdscr.addstr('Word count: ' + str(count) + '\n')
    stdscr.addstr('Time: ' + str(round(end - start)) + ' seconds\n')
    stdscr.addstr('WPM: ' + str(int(round((count / (end - start)) * 60))) + '\n\n')
    stdscr.addstr('Press any key to play again...' + '\n')
    render_bottom_menu(stdscr)
    return stdscr.getch()

def get_text(max_tries, count):
    """ Get text challenge """
    # Use fallback text if wikipedia fails to deliver
    if count > max_tries:
        return 'Mercury is the smallest and innermost planet in the Solar System'
    # Get a random wiki page
    random = wikipedia.random(1)
    try:
        # Get summary of page
        page = wikipedia.page(random).summary
    except wikipedia.exceptions.DisambiguationError:
        page = get_text(max_tries, count + 1)
    return page

curses.wrapper(main)
