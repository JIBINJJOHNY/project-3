import curses
from random import randint
from time import sleep
import gspread
from google.oauth2.service_account import Credentials


def main(stdscr):
    """
    main function that controls the game. It receives a stdscr object which represents the game screen.
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
