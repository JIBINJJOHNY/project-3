import curses
from simple_term_menu import TerminalMenu
import gspread
from google.oauth2.service_account import Credentials
from snake_easy import main as snake_easy_main
from snake_medium import main as snake_medium_main
from snake_hard import main as snake_hard_main


class GameMenu:
    def __init__(self):
        # Initialize the main menu using TerminalMenu
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
        show_menu method displays the main menu and
        stores the chosen menu option's index in current_state

        """
    
        menu_entry_index = self.menu.show()
        self.current_state = menu_entry_index

    def show_levels_menu(self):
        """
        show_levels_menu method displays a submenu for selecting game
          levels and updates current_state
        """
        sub_options = ["Easy", "Medium", "Hard", "Back"]
        sub_menu = TerminalMenu(sub_options, title="LEVELS")  
        sub_menu_entry_index = sub_menu.show()  # Display the submenu
        self.current_state = sub_menu_entry_index

    def show_instructions(self):
        """
        show_instructions method displays the game instructions and
        provides options to return to the main menu.
        """
        self.instruction_menu = TerminalMenu(["Back"])
        instructions = [
        "Slithering Challenge!",
        "",
        "How to Play:",
        "1. Use the arrow keys (Up, Down, Left, Right)to control the snake's movement.",
        "2. Your goal is to collect the red food items to increase your score and grow your snake's length.",
        "3. Be cautious not to run into the walls or collide with your own body, as this will cost you a life.",
        "4. The snake's length will increase with each collected food, making it both a reward and a challenge to manage.",
        "",
        "Game Elements:",
        "- Snake: Control the snake's movement with the arrow keys. The snake's head is denoted by a '#', and yellow color'.",
        "- Red Food: Collect the red food represented by '*'. Each collected food adds to your score and length.",
        "- Walls: The game area is bordered by walls. Colliding with them results in the loss of a life.",
        "- Lives: You start with three lives. Losing all lives will end the game.",
        "- Pause: Press 'Esc' at any time to pause the game and catch your breath. Resume by pressing any key.",
        "",
        "Scoring:",
        "- Each collected food adds one point to your score.",
        "- The longer your snake, the faster it moves, adding a strategic challenge to the game.",
        "",
        "After the Game:",
        "- Once you run out of lives, the game ends, and you'll be presented with options.",
        "- Press 'Yes' to save your score and see the leaderboard, competing with others for the top spot.",
        "- Press 'No' to return to the level selection screen.",
        "- Press '0' to go back to the main menu and explore other game options.",
        "",
        "Tips:",
        "- Plan your movements carefully to avoid collisions with walls and your snake's body.",
        "- Keep an eye on the snake's length; a longer snake requires more precise maneuvers.",
        "",
        "Enjoy the challenge and strive to top the leaderboard!"
    ]

        back_menu = TerminalMenu(["Back"])
        while True:
            print("\n".join(instructions))
            user_input = back_menu.show()
            if user_input == 0:
                self.show_menu()
                break

    def choose_leaderboard_level(self):
        """
        choose_leaderboard_level method prompts the user to choose a
        leaderboard level.
        """
        sub_options = ["Easy", "Medium", "Hard", "Back"]
        sub_menu = TerminalMenu(sub_options, title="Which level's leaderboard do you want to see?")  
        sub_menu_entry_index = sub_menu.show()  # Display the submenu
        return sub_menu_entry_index

    def show_leaderboard(self):
        """
        show_leaderboard method displays the chosen leaderboard or goes back
        to the main menu.
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
        display_leaderboard method fetches and displays the leaderboard data
        for a specific level.
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

        except Exception as e:
            print("Error fetching or displaying leaderboard data:", str(e))

    def start_game(self):
        """
        start_game method contains the main game loop which
        responds to the user's menu choices and starts the game
        or displays instructions/leaderboards.
        """
        while True:
            if self.current_state == 0:
                self.show_levels_menu()

                if self.current_state == 0:
                    self.start_easy_level()

                elif self.current_state == 1:
                    self.start_medium_level()


                elif self.current_state == 2:
                    self.start_hard_level()

                elif self.current_state == 3:
                    self.show_menu()  # Go back to main menu

            elif self.current_state == 1:
                self.show_instructions()

            elif self.current_state == 2:
                self.show_leaderboard()

            elif self.current_state == 3:
                break  # Quit the game

    def start_snake_game(self, game_function):
        """
        start_snake_game method is a wrapper that starts the snake game using
        the provided game function and the curses module
        """
        curses.wrapper(game_function)

    def start_easy_level(self):
        """
        start_easy_level method starts the snake game for the easy level
        """
        self.start_snake_game(snake_easy_main)
        self.show_levels_menu()  # Go back to level selection after the game

    def start_medium_level(self):
        """
        start_medium_level method starts the snake game for the medium level
        """
        self.start_snake_game(snake_medium_main)
        self.show_levels_menu()  # Go back to level selection after the game

    def start_hard_level(self):
        """
        start_hard_level method starts the snake game for the hard level
        """
        self.start_snake_game(snake_hard_main)
        self.show_levels_menu()
    def start(self):
        """
        The start method initializes the main menu and begins the game loop.
        """
        print("Welcome to Slithering Challenge\n")  # Heading
        self.show_menu()
        self.start_game()


def main():
    """
    The main function creates an instance of GameMenu and starts the game menu.
    """
    game_menu = GameMenu()
    game_menu.start()

if __name__ == "__main__":
    main()
