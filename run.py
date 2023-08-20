import os
from snake_easy import main as snake_easy_main
from snake_medium import main as snake_medium_main
from snake_hard import main as snake_hard_main
import gspread
from google.oauth2.service_account import Credentials

class GameMenu:
    def __init__(self):
        self.SCOPE = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive",
        ]
        self.CREDS = Credentials.from_service_account_file("creds.json")
        self.SCOPED_CREDS = self.CREDS.with_scopes(self.SCOPE)
        self.GSPREAD_CLIENT = gspread.authorize(self.SCOPED_CREDS)
        self.SHEET = self.GSPREAD_CLIENT.open("slithering_challenge")

    def show_menu(self):
        print("Welcome to Slithering Challenge\n")
        while True:
            print("Main Menu:")
            print("1. Start Game")
            print("2. Instructions")
            print("3. Leaderboard")
            print("4. Quit")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.display_levels_menu()
            elif choice == "2":
                self.display_instructions()
            elif choice == "3":
                self.display_leaderboard()
            elif choice == "4":
                print("Thank you for playing! See you soon!")
                break
            else:
                print("Invalid choice. Please choose a valid option.")

    def show_levels_menu(self):
        print("\nSelect a Level:")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")
        print("4. Back")

        choice = input("Enter your choice: ")

        if choice == "1":
            self.start_snake_game(snake_easy_main)
        elif choice == "2":
            self.start_snake_game(snake_medium_main)
        elif choice == "3":
            self.start_snake_game(snake_hard_main)
        elif choice == "4":
            pass
        else:
            print("Invalid choice. Please choose a valid option.")

    def show_instructions(self):
        """
        Show_instructions method displays the game instructions and
        provides options to return to the main menu.
        """
        print(
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
        )
        input("Press Enter to go back to the main menu.")

    def show_leaderboard_menu(self):
        print("\nLeaderboard:")
        while True:
            print("1. Easy Leaderboard")
            print("2. Medium Leaderboard")
            print("3. Hard Leaderboard")
            print("4. Back to Main Menu")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.display_leaderboard("easy")
            elif choice == "2":
                self.display_leaderboard("medium")
            elif choice == "3":
                self.display_leaderboard("hard")
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please choose a valid option.")

    def display_leaderboard(self, level_name):
        try:
            level_worksheet = self.SHEET.worksheet(level_name)
            level_data = level_worksheet.get_all_values()

            sorted_level_data = sorted(
                (
                    entry for entry in level_data[1:] if entry[1]
                ),
                key=lambda x: int(x[1]),
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
        MENU_MAIN = "main"
        MENU_LEVELS = "levels"
        MENU_INSTRUCTIONS = "instructions"
        MENU_LEADERBOARD = "leaderboard"
        MENU_QUIT = "quit"
        MENU_GAME_OVER = "game_over"

        current_menu = MENU_MAIN

        while True:
            if current_menu == MENU_MAIN:
                self.show_menu()

                if self.current_state == 0:
                    current_menu = MENU_LEVELS

                elif self.current_state == 1:
                    current_menu = MENU_INSTRUCTIONS

                elif self.current_state == 2:
                    current_menu = MENU_LEADERBOARD

                elif self.current_state == 3:
                    current_menu = MENU_QUIT

            elif current_menu == MENU_LEVELS:
                self.show_levels_menu()

                if self.current_state == 0:
                    self.start_easy_level()

                elif self.current_state == 1:
                    self.start_medium_level()

                elif self.current_state == 2:
                    self.start_hard_level()

                elif self.current_state == 3:
                    current_menu = MENU_MAIN

            elif current_menu == MENU_INSTRUCTIONS:
                self.dispaly_instructions()
                current_menu = MENU_MAIN
                

            elif current_menu == MENU_LEADERBOARD:
                self.display_leaderboard()
                current_menu = MENU_MAIN

            elif current_menu == MENU_QUIT:
                print("Thank you for playing! See you soon!")
                break  # Quit the game

            elif current_menu == MENU_GAME_OVER:
                self.display_levels_menu()  # Go back to level selection
                current_menu = MENU_LEADERBOARD

    def start_snake_game(self, game_function):
        os.system('cls' if os.name == 'nt' else 'clear')
        game_function()

    def start(self):
        self.show_menu()

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    game_menu = GameMenu()
    game_menu.start()


if __name__ == "__main__":
    main()