import curses
from random import randint
from time import sleep
import gspread
from google.oauth2.service_account import Credentials


def main(stdscr):
    """
    main function It sets up the terminal window,
    initializes the game variables such as
    the snake's position, food position, score, and lives
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
    ESC = 27
    key = curses.KEY_RIGHT
    prev_key = key

    score = 0
    lives = 3
