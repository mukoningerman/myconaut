"""
Myconaut - Main Entry Point
"""

import sys
import os

# Add parent directory to path for config import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from ascii_art import ASCIIArt
from game import Game

def main_menu():
    """Display main menu"""
    game = Game()

    while True:
        Config.clear_screen()
        print(ASCIIArt.title_screen())

        # Display menu options
        options = [
            ("1", "New Game", "Start a new adventure"),
            ("2", "Load Game", "Continue with password"),
            ("3", "How to Play", "Game instructions"),
            ("4", "About", "Game information"),
            ("5", "Credits", "Meet the creators"),
            ("6", "Exit", "Leave the game")
        ]

        Config.print_colored("\nMain Menu:\n", 'highlight')

        for key, action, desc in options:
            Config.print_colored(f"  [{key}] {action:15} - {desc}", 'normal')

        choice = input("\nChoose option: ").strip()

        if choice == "1":
            game.start_new_game()
            game.main_loop()
        elif choice == "2":
            load_game_menu(game)
        elif choice == "3":
            how_to_play()
        elif choice == "4":
            about_game()
        elif choice == "5":
            show_credits()
        elif choice == "6":
            Config.print_colored("\nThank you for playing Myconaut!", 'title')
            Config.print_colored("May balance guide your path.", 'highlight')
            sys.exit(0)
        else:
            Config.print_colored("Invalid choice!", 'error')
            input("\nPress Enter to continue...")

def load_game_menu(game):
    """Display load game menu"""
    Config.clear_screen()

    Config.print_colored(ASCIIArt.create_box("LOAD GAME"), 'title')
    Config.print_colored("\nEnter your save password:", 'info')
    Config.print_colored("(Or enter '0' to return to main menu)", 'info')

    password = input("\nPassword: ").strip()

    if password == "0":
        return

    if game.load_game(password):
        game.main_loop()
    else:
        Config.print_colored("\nFailed to load game. Please check your password.", 'error')
        input("\nPress Enter to continue...")

def how_to_play():
    """Display game instructions"""
    Config.clear_screen()

    Config.print_colored(ASCIIArt.create_box("HOW TO PLAY"), 'title')

    instructions = """
    Myconaut is a text-based adventure where you explore a world of
    plants and fungi. Your goal is to restore balance to the ecosystem.

    BASIC CONTROLS:
    • Use NUMBER KEYS (1, 2, 3...) or LETTERS (N, S, E, W) to choose actions
    • Press ENTER to confirm selections
    • Explore locations to find items
    • Talk to NPCs for quests and information
    • Use items from your inventory

    GAMEPLAY:
    1. COLLECT resources (plants, mushrooms)
    2. CRAFT potions and items using alchemy
    3. COMPLETE quests for experience and rewards
    4. DEFEAT enemies in turn-based combat
    5. DISCOVER the story through exploration

    COMBAT:
    • You and enemies take turns attacking
    • Use ABILITIES that cost mana
    • Use ITEMS from inventory during combat
    • Try to ESCAPE if the fight is too hard

    ALCHEMY:
    • Combine plants and mushrooms to create new items
    • Discover new recipes through experimentation
    • Some recipes are taught by NPCs

    HALLUCINATIONS:
    • Certain mushrooms can alter your perception
    • Hallucinations reveal hidden secrets
    • But be careful - too much can be dangerous!

    SAVING:
    • Your game is saved with a PASSWORD
    • Write down the password to continue later
    • Passwords are also saved in the 'saves' folder
    """

    print(Config.COLORS['normal'] + instructions)
    input("\nPress Enter to return to main menu...")

def about_game():
    """Display game information"""
    Config.clear_screen()

    Config.print_colored(ASCIIArt.create_box("ABOUT MYCONAUT"), 'title')

    about_text = f"""
    {Config.COLORS['title']}Myconaut v{Config.VERSION}{Config.COLORS['normal']}

    A psychedelic fungal adventure about balance and harmony.

    In a world where plants and fungi are at war, you must
    discover the truth about their symbiotic relationship.
    Collect resources, brew potions, and make choices that
    determine the fate of the ecosystem.

    {Config.COLORS['highlight']}THEMES:{Config.COLORS['normal']}
    • Balance and harmony
    • Symbiosis vs. parasitism
    • Perception vs. reality
    • Consequences of choices

    {Config.COLORS['highlight']}FEATURES:{Config.COLORS['normal']}
    • Colorful ASCII graphics
    • Turn-based combat system
    • Alchemy crafting system
    • Psychedelic hallucination effects
    • Multiple endings
    • Password-based save system

    {Config.COLORS['highlight']}GAME LENGTH:{Config.COLORS['normal']}
    • Main story: 3-5 hours
    • Completionist: 5-7 hours
    • Multiple playthroughs encouraged

    Created with passion by {Config.AUTHOR}
    """

    print(about_text)

    Config.print_colored("\nSupport the developer:", 'highlight')
    Config.print_colored(f"BTC:  {Config.DONATION_BTC}", 'info')
    Config.print_colored(f"ETH:  {Config.DONATION_ETH}", 'info')
    Config.print_colored(f"USDT: {Config.DONATION_USDT}", 'info')

    input("\nPress Enter to return to main menu...")

def show_credits():
    """Display game credits"""
    Config.clear_screen()

    Config.print_colored(ASCIIArt.create_box("CREDITS"), 'title')

    credits = f"""
    {Config.COLORS['title']}MYCONAUT{Config.COLORS['normal']}

    {Config.COLORS['highlight']}Created by:{Config.COLORS['normal']}
    • {Config.AUTHOR}

    {Config.COLORS['highlight']}Contact:{Config.COLORS['normal']}
    • Email: {Config.EMAIL}

    {Config.COLORS['highlight']}Special Thanks:{Config.COLORS['normal']}
    • The mycology community
    • Text adventure enthusiasts
    • Beta testers
    • Open source contributors

    {Config.COLORS['highlight']}Tools Used:{Config.COLORS['normal']}
    • Python 3
    • Colorama library
    • ASCII art generators
    • VS Code

    {Config.COLORS['highlight']}Inspired by:{Config.COLORS['normal']}
    • Classic text adventures
    • Mycology and botany
    • Psychedelic art
    • Environmental stories

    Thank you for playing!
    Remember: Every plant and fungus has its place.
    """

    print(credits)
    input("\nPress Enter to return to main menu...")

def main():
    """Main function"""
    try:
        main_menu()
    except KeyboardInterrupt:
        Config.print_colored("\n\nGame interrupted. Farewell!", 'info')
        sys.exit(0)
    except Exception as e:
        Config.print_colored(f"\nAn error occurred: {e}", 'error')
        Config.print_colored("Please report this issue to the developer.", 'info')
        input("\nPress Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
