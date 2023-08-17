import curses
from simple_term_menu import TerminalMenu
import gspread
from google.oauth2.service_account import Credentials


class GameMenu:
    def __init__(self):
        # Initialize the main menu using TerminalMenu
        self.menu = TerminalMenu(["Start Game", "Instructions", "Leaderboard", "Quit"])
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
        show_menu method displays the main menu and stores the chosen menu option's index in current_state

        """
        print("Welcome to Slithering Challenge\n")  # Heading
        menu_entry_index = self.menu.show()
        self.current_state = menu_entry_index

    def show_levels_menu(self):
        """
        show_levels_menu method displays a submenu for selecting game levels and updates current_state
        """
        heading = "Levels"
        sub_options = ["Easy", "Medium", "Hard", "Back"]
        sub_menu = TerminalMenu(sub_options)  # Create a submenu
        sub_menu_entry_index = sub_menu.show()  # Display the submenu
        self.current_state = sub_menu_entry_index
