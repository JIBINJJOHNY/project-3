import curses
from random import randint
from time import sleep
from colorama import init, Fore, Back, Style 
import gspread
from google.oauth2.service_account import Credentials


def main(stdscr):
    """
    main function It sets up the terminal window,
    initializes the game variables such as
    the snake's position, food position, score, and lives
    """
    stdscr.clear()
    init(autoreset=True) 
    curses.start_color()  # Initialize color pairs in curses
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Snake color
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)  # Food color
    sh = 20
    sw = 60
   
    win = curses.newwin(sh + 1, sw + 1, 0, 0)
    win.keypad(1)
    curses.noecho()
    #curses.curs_set(0)
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
        # Move the snake forward
        snake.insert(0, (y, x))
        # Generate new food if none exists
        if not food:
            while True:
                food = (
                    randint(1, sh - 1),
                    randint(1, sw - 1),
                )
                if food not in snake:
                    break
            win.addch(food[0], food[1], "*", curses.A_BOLD | curses.color_pair(2))  # Display the food
        # Check if snake has eaten the food
        elif snake[0] == food:
            score += 1
            food = ()  # Clear the food position
        else:
            last = snake.pop()
            win.addch(last[0], last[1], " ")  # Clear the tail position

        win.addch(snake[0][0], snake[0][1], "#", curses.A_BOLD | curses.color_pair(1))  # Display the snake's head

    # Clear the window before displaying the game over message
    win.clear()
    win.addstr(sh // 2 - 1, sw // 2 - 10, "Game Over", curses.A_BOLD)
    win.addstr(sh // 2, sw // 2 - 10, f"Final Score: {score}", curses.A_BOLD)
    win.refresh()

    # Wait for a key press
    win.getch()
    # Add a delay before displaying the save score prompt
    sleep(3)

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
        win.refresh()  # Refresh the screen to display the prompt
        save_choice = win.getch()

    SCOPE = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]
    # Initialize current_user_name
    current_user_name = ""
    if save_choice == ord("y"):
        win.clear()
        win.addstr(sh // 2, sw // 2 - 15, "Enter your name:", curses.A_BOLD)
        win.refresh()

        # Get the user's name input
        name = ""
        name_row = sh // 2 + 1  # Calculate the row for displaying the name
        name_col = sw // 2 - 15  # Calculate the column for displaying the name
        while True:
            char = win.getch()
            if char == 10:  # Enter key
                break
            elif 32 <= char <= 126:  # ASCII printable characters
                name += chr(char)
                win.addstr(name_row, name_col, name, curses.A_NORMAL)
        # Refresh the screen once after the name has been entered
        win.refresh()

        # Assign the name to current_user_name
        current_user_name = name
    # Clear the window again before displaying the top scorers list
    win.clear()

    # Fetch and sort the top scorers regardless of saving choice
    try:
        CREDS = Credentials.from_service_account_file("creds.json")
        SCOPED_CREDS = CREDS.with_scopes(SCOPE)
        GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
        SHEET = GSPREAD_CLIENT.open("slithering_challenge")
        easy = SHEET.worksheet("easy")
        easy.append_row([name, score])
        top_scorers = easy.get_all_values()[1:]
        sorted_top_scorers = sorted(top_scorers, key=lambda x: int(x[1]), reverse=True)
    except Exception as e:
        # Handle any errors that might occur during the API call
        win.addstr(sh // 2, sw // 2 - 15, "Error fetching top scorers.", curses.A_BOLD)
        win.addstr(sh // 2 + 1, sw // 2 - 15, str(e))
        win.refresh()
    # Display the top 10 scorers list

    try:
        win.clear()  # Clear the window before displaying the top scorers list
        win.addstr(sh // 2 - 5, sw // 2 - 15, "Top 10 Scorers", curses.A_BOLD)
        # Variable to track if the current user's entry is highlighted
        current_user_highlighted = False
        for i, (name, s) in enumerate(sorted_top_scorers[:10], start=1):
            position_str = f"{i}. {name}: {s}"
            if name == current_user_name and int(s) == score:
                # Highlight the current user's entry
                win.addstr(
                    sh // 2 - 5 + i, sw // 2 - 15, position_str, curses.A_STANDOUT
                )
                current_user_highlighted = True
            else:
                win.addstr(sh // 2 - 5 + i, sw // 2 - 15, position_str)
        if not current_user_highlighted and len(sorted_top_scorers) < 10:
            i += 1
            # highlight name and score
            position_str = f"{i}. {current_user_name}: {score}"
            win.addstr(
                sh // 2 - 5 + i, sw // 2 - 15, position_str, curses.A_STANDOUT
                )
        win.refresh()
        win.getch()
        # Add a delay to allow the user more time to view the content
        sleep(10)
    except Exception as e:
        # Handle any errors that might occur during the API call
        win.clear()
        win.addstr(
            sh // 2, sw // 2 - 15, "Error fetching top scorers.", curses.A_BOLD
            )
        win.addstr(sh // 2 + 1, sw // 2 - 15, str(e))
        win.refresh()


# Function is used to safely run the main function,
#  setting up and cleaning up the terminal environment correctly.
if __name__ == "__main__":
    curses.wrapper(main)
