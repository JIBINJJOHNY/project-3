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
