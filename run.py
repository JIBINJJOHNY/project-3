import os
import curses
from simple_term_menu import TerminalMenu
import gspread
from google.oauth2.service_account import Credentials
from snake_easy import main as snake_easy_main
from snake_medium import main as snake_medium_main
from snake_hard import main as snake_hard_main


class GameMenu:
    # Constants for different menu states
    MENU_MAIN = "main"
    MENU_LEVELS = "levels"
    MENU_INSTRUCTIONS = "instructions"
    MENU_LEADERBOARD = "leaderboard"
    MENU_QUIT = "quit"
    MENU_GAME_OVER = "game_over"

    def __init__(self):
        """
        Initialize the main menu using TerminalMenu
        """
        self.menu = TerminalMenu(
            ["Start Game", "Instructions", "Leaderboard", "Quit"]
            )
        # OAuth2 scopes for Google Sheets and Drive API
        self.SCOPE = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive",
        ]
        self.CREDS = Credentials.from_service_account_file("creds.json")
        self.SCOPED_CREDS = self.CREDS.with_scopes(self.SCOPE)
        self.GSPREAD_CLIENT = gspread.authorize(self.SCOPED_CREDS)
        self.SHEET = self.GSPREAD_CLIENT.open("slithering_challenge")
        self.current_state = None

    def show_menu(self):
        """
        The show_menu method displays the main menu using
        the TerminalMenu instance created earlier.
        It listens for user input and sets the
        current menu state accordingly.
        """
        menu_entry_index = self.menu.show()
        self.current_menu = self.MENU_MAIN

        if menu_entry_index == 0:
            self.current_menu = self.MENU_LEVELS
        elif menu_entry_index == 1:
            self.show_instructions()
        elif menu_entry_index == 2:
            self.show_leaderboard()
        elif menu_entry_index == 3:
            self.current_menu = self.MENU_QUIT

    def show_levels_menu(self):
        """
        The show_levels_menu method displays a submenu for
        selecting game levels.It listens for user input and
        starts the corresponding snake game level using the
        appropriate function based on the user's selection.
        """
        sub_options = ["Easy", "Medium", "Hard", "Back"]
        sub_menu = TerminalMenu(sub_options, title="LEVELS")
        sub_menu_entry_index = sub_menu.show()
        self.current_menu = self.MENU_LEVELS

        if sub_menu_entry_index == 0:
            self.start_snake_game(snake_easy_main)
            self.current_menu = self.MENU_LEVELS
        elif sub_menu_entry_index == 1:
            self.start_snake_game(snake_medium_main)
            self.current_menu = self.MENU_LEVELS
        elif sub_menu_entry_index == 2:
            self.start_snake_game(snake_hard_main)
            self.current_menu = self.MENU_LEVELS
        elif sub_menu_entry_index == 3:
            self.current_menu = self.MENU_MAIN

    def show_instructions(self):
        """
        Show_instructions method displays the game instructions and
        provides options to return to the main menu.
        """
        self.instruction_menu = TerminalMenu(["Back"])
        instructions = [
            "Slithering Challenge!",
            "",
            "How to Play:",
            "1. Use the arrow keys(Up, Down, Left, Right)to control the snake",
            "2. Your goal is to collect the red food items to increase your.",
            "3. Be cautious avoid walls or collide with your own body,",
            "   as this will cost you a life.",
            "4. The snake's length will increase with each collected food,",
            "   making it both a reward and a challenge to manage.",
            "",
            "Game Elements:",
            "- Snake: Control the snake's movement with the arrow keys.",
            "         The snake's head is denoted by a '#',and yellow color'.",
            "- Red Food: Collect the red food represented by '*'.",
            "            Each collected food adds to your score and length.",
            "- Walls: The game area is bordered by walls.",
            "         Colliding with them results in the loss of a life.",
            "- obstacles: Medium and Hard levels contain obstacles.",
            "- Lives: You start with three lives.",
            "         Losing all lives will end the game.",
            "- Pause: Press 'Esc' at any time to pause the game",
            "         Resume by pressing any key.",
            "",
            "Scoring:",
            "- Each collected food adds one point to your score.",
            "- The longer your snake, the faster it moves,",
            "  adding a strategic challenge to the game.",
            "",
            "After the Game:",
            "- Once you run out of lives, the game ends,",
            "  and you'll be presented with options.",
            "- Press 'Yes' to save your score and see the leaderboard,",
            "  competing with others for the top spot.",
            "- Press 'No' to return to the level selection screen.",
            "",
            "Tips:",
            "- Plan your movements carefully to avoid collisions with walls",
            "  and your snake's body.",
            "- Keep an eye on the snake's length;",
            "  a longer snake requires more precise maneuvers.",
            "",
            "Enjoy the challenge and strive to top the leaderboard!"
        ]
        back_menu = TerminalMenu(["Back"])
        while True:
            print("\n".join(instructions))
            user_input = back_menu.show()
            if user_input == 0:
                os.system('cls' if os.name == 'nt' else 'clear')
                self.show_menu()
                break

    def choose_leaderboard_level(self):
        """
        choose_leaderboard_level method prompts the user to choose a
        leaderboard level.by displaying a submenu.
        It returns the index of the user's selection.
        """
        sub_options = ["Easy", "Medium", "Hard", "Back"]
        sub_menu = TerminalMenu(
            sub_options, title="Which level's leaderboard do you want to see?"
            )
        sub_menu_entry_index = sub_menu.show()  # Display the submenu
        return sub_menu_entry_index

    def show_leaderboard(self):
        """
        The show_leaderboard method displays the leaderboard submenu
        and reacts based on user input. If a valid level is selected,
        it fetches and displays the leaderboard data for that level using
        the display_leaderboard method. If "Back" is selected,
        it returns to the main menu.
        """
        level_menu_entry_index = self.choose_leaderboard_level()

        if level_menu_entry_index in [0, 1, 2]:
            level_names = ["easy", "medium", "hard"]
            level_name = level_names[level_menu_entry_index]
            self.display_leaderboard(level_name)

        elif level_menu_entry_index == 3:
            self.show_menu()  # Go back to main menu

    def display_leaderboard(self, level_name):
        """
        The display_leaderboard method fetches and displays the leaderboard
        data for a specific level. After the data is displayed,
        it waits for the user to press "Back" and clears the screen before
        going back to the leaderboard submenu.
        """
        try:
            level_worksheet = self.SHEET.worksheet(level_name)
            level_data = level_worksheet.get_all_values()

            # Sort the level data by score in descending order
            sorted_level_data = sorted(
                (
                    entry for entry in level_data[1:] if entry[1]
                ),  # Filter out entries with empty scores
                key=lambda x: int(x[1]),  # Convert to integer for sorting
                reverse=True,
            )

            print(f"Displaying {level_name.capitalize()} level leaderboard:")
            for rank, entry in enumerate(sorted_level_data, start=1):
                name, score = entry
                print(f"{rank}. {name}: {score}")
            back_menu = TerminalMenu(["Back"])
            user_input = back_menu.show()
            if user_input == 0:
                os.system('cls' if os.name == 'nt' else 'clear')
                self.show_leaderboard()

        except Exception as e:
            print("Error fetching or displaying leaderboard data:", str(e))

    def start_game(self):
        """
        The start_game method starts the game loop. It continuously checks
        the current menu state and displays the appropriate menu or executes
        the corresponding game logic based on the user's input.
        """
        while self.current_menu != self.MENU_QUIT:
            if self.current_menu == self.MENU_MAIN:
                self.show_menu()
            elif self.current_menu == self.MENU_LEVELS:
                self.show_levels_menu()

            elif self.current_menu == self.MENU_INSTRUCTIONS:
                self.show_instructions()

            elif self.current_menu == self.MENU_QUIT:
                print("Thank you for playing! See you soon!")
                break

            elif self.current_menu == self.MENU_GAME_OVER:
                self.show_levels_menu()
                self.current_menu = self.MENU_LEVELS

    def start_snake_game(self, game_function):
        """
        The start_snake_game method starts the specified snake
        game level using the curses library.
        """

        curses.wrapper(game_function)

    def start(self):
        """
        The start method initializes the game by displaying
        a welcome message, showing the main menu,
        and starting the game loop.
        """
        print("Welcome to Slithering Challenge\n")
        self.show_menu()
        self.start_game()


def main():
    """
    The main function clears the screen, creates an instance
    of the GameMenu class, and starts the game by calling the
    start method.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    game_menu = GameMenu()
    game_menu.start()


if __name__ == "__main__":
    main()
    