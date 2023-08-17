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
        if not food:
            while True:
                food = (
                    randint(1, sh - 1),
                    randint(1, sw - 1),
                )
                if food not in snake and food not in obstacles:
                    break
            win.addch(food[0], food[1], "*")
        elif snake[0] == food:
            score += 1
            food = ()
        else:
            last = snake.pop()
            win.addch(last[0], last[1], " ")

        for obstacle in obstacles:
            win.addch(obstacle[0], obstacle[1], "X")

        win.addch(snake[0][0], snake[0][1], "#")
        win.addch(snake[0][0], snake[0][1], "#")
        # Calculate the timeout value for controlling snake speed
        # Increase this value to slow down the snake
        timeout_value = 100 - (len(snake)) // 5 + len(snake) // 30 % 160
        # Set the timeout value
        win.timeout(timeout_value)
    # Clear the window before displaying the game over message
    win.clear()
    win.addstr(sh // 2 - 1, sw // 2 - 10, "Game Over", curses.A_BOLD)
    win.addstr(sh // 2, sw // 2 - 10, f"Final Score: {score}", curses.A_BOLD)
    win.refresh()

    # Wait for a key press
    win.getch()

    # Add a delay here before displaying the save score prompt
    time.sleep(3)  # Change the delay time according to your preference

    # Clear the window again before displaying the prompt
    win.clear()

    # Display the save score prompt and options
    win.addstr(
        sh // 2 - 2, sw // 2 - 15, "Do you want to save your score?", curses.A_BOLD
    )
    win.addstr(sh // 2, sw // 2 - 6, "Yes", curses.A_BOLD)
    win.addstr(sh // 2, sw // 2 + 1, "No", curses.A_BOLD)
    win.refresh()
    # Get user input for saving score
    save_choice = None
    while save_choice not in [ord("y"), ord("n")]:
        save_choice = win.getch()
