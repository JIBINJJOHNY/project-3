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
        # Handle user input and snake movement
        event = win.getch()
        if event != -1:
            # Process user input to change snake direction
            if event == curses.KEY_DOWN and prev_key != curses.KEY_UP:
                key = curses.KEY_DOWN
            if event == curses.KEY_UP and prev_key != curses.KEY_DOWN:
                key = curses.KEY_UP
            if event == curses.KEY_LEFT and prev_key != curses.KEY_RIGHT:
                key = curses.KEY_LEFT
            if event == curses.KEY_RIGHT and prev_key != curses.KEY_LEFT:
                key = curses.KEY_RIGHT

        prev_key = key

        y, x = snake[0]

        if key == curses.KEY_DOWN and prev_key != curses.KEY_UP:
            y += 1
        if key == curses.KEY_UP and prev_key != curses.KEY_DOWN:
            y -= 1
        if key == curses.KEY_LEFT and prev_key != curses.KEY_RIGHT:
            x -= 1
        if key == curses.KEY_RIGHT and prev_key != curses.KEY_LEFT:
            x += 1

        if y == 0 or y == sh or x == 0 or x == sw:
            lives -= 1
            if lives == 0:
                break
            else:
                time.sleep(1)
                continue

        if (y, x) in snake[1:]:
            lives -= 1
            if lives == 0:
                break
            else:
                hit_index = snake.index((y, x))
                snake = snake[
                    : hit_index + 1
                ]  # Keep only the collided part of the snake
                snake[0] = (y, x)  # Update the head position
                time.sleep(1)
                continue
        if (y, x) in obstacles:
            lives -= 1
            if lives == 0:
                break
            else:
                time.sleep(1)
                continue

        snake.insert(0, (y, x))
