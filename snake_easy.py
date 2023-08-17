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

    while key != ESC and lives > 0:
        # Display the score and lives on the screen
        win.addnstr(0, 2, "Score: " + str(score) + " ", 20)
        win.addnstr(0, sw - 10, "Lives: " + str(lives) + " ", 20)
        win.timeout(150 - (len(snake)) // 5 + len(snake) // 10 % 120)
        event = win.getch()

        # Handle user input to change the snake's direction
        if event != -1:
            if event == curses.KEY_DOWN and prev_key != curses.KEY_UP:
                key = curses.KEY_DOWN
            if event == curses.KEY_UP and prev_key != curses.KEY_DOWN:
                key = curses.KEY_UP
            if event == curses.KEY_LEFT and prev_key != curses.KEY_RIGHT:
                key = curses.KEY_LEFT
            if event == curses.KEY_RIGHT and prev_key != curses.KEY_LEFT:
                key = curses.KEY_RIGHT

        prev_key = key

        # Update snake's position based on key input
        y, x = snake[0]
        if key == curses.KEY_DOWN and prev_key != curses.KEY_UP:
            y += 1
        if key == curses.KEY_UP and prev_key != curses.KEY_DOWN:
            y -= 1
        if key == curses.KEY_LEFT and prev_key != curses.KEY_RIGHT:
            x -= 1
        if key == curses.KEY_RIGHT and prev_key != curses.KEY_LEFT:
            x += 1

        # Teleport the snake to the opposite edge if it goes out of bounds
        if y == 0:
            y = sh - 1
        elif y == sh:
            y = 1
        if x == 0:
            x = sw - 1
        elif x == sw:
            x = 1

        if (y, x) in snake[1:]:
            # Snake collided with itself
            lives -= 1
            if lives == 0:
                break
            else:
                # Pause briefly before continuing
                sleep(1)
                continue
