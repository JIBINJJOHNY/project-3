import curses
from random import randint
from time import sleep, time
import gspread
from google.oauth2.service_account import Credentials


def main(stdscr):
    """
    The main function is the entry point of the program.
    It receives the stdscr object, which represents the game screen.
    """
    stdscr.clear()
    sh = 20
    sw = 60

    win = curses.newwin(sh + 1, sw + 1, 0, 0)
    win.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    win.border(0)
    win.nodelay(1)

    snake = [(sh // 2, sw // 2), (sh // 2, sw // 2 - 1), (sh // 2, sw // 2 - 2)]
    food = ()
    obstacles = [
        (sh // 2 - 3, sw // 2),
        (sh // 2 + 3, sw // 2),
        (sh // 2, sw // 2 - 10),
        (sh // 2 - 5, sw // 2 + 5),
        (sh // 2 + 5, sw // 2 - 7),
    ]
    ESC = 27
    key = curses.KEY_RIGHT
    prev_key = key

    score = 0
    lives = 3
    timer_start = time()  # Timer start time
    timer_duration = 120  # 2 minutes in seconds

    while key != ESC and lives > 0:
        # Calculate the time remaining on the timer
        time_remaining = timer_duration - (time() - timer_start)
        minutes = int(time_remaining // 60)
        seconds = int(time_remaining % 60)

        # Display the game information
        win.addnstr(0, 2, "Score: " + str(score) + " ", 20)
        win.addnstr(0, sw - 10, "Lives: " + str(lives) + " ", 20)
        win.addnstr(0, sw // 2 - 7, f"Time: {minutes:02d}:{seconds:02d}", 20)

        # Check if the timer has run out
        if time_remaining <= 0:
            lives = 0  # User loses when the timer runs out
            break
