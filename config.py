"""
Myconaut - Configuration File
Author: mukoningerman
Email: mukonin.german@icloud.com
"""

import os
from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)

# Game configuration
class Config:
    # Game info
    GAME_NAME = "Myconaut"
    VERSION = "1.0.0"
    AUTHOR = "mukoningerman"
    EMAIL = "mukonin.german@icloud.com"

    # Donation addresses
    DONATION_BTC = "bc1qslvfy88nzz99pl8uhdc3v5ynje6qs7csfhveyn"
    DONATION_ETH = "0xB00541cf0C6745ad24A31c502D6B0BA19d7E8c9A"
    DONATION_USDT = "TTcjEmDYgEwYhE3Qm78rNS6yNnCCj5QYVS"

    # Display settings
    SCREEN_WIDTH = 80
    SCREEN_HEIGHT = 30
    TYPEWRITER_DELAY = 0.03  # seconds

    # Colors
    COLORS = {
        'title': Fore.MAGENTA + Style.BRIGHT,
        'normal': Fore.WHITE,
        'highlight': Fore.YELLOW + Style.BRIGHT,
        'success': Fore.GREEN,
        'warning': Fore.YELLOW,
        'error': Fore.RED,
        'info': Fore.CYAN,
        'magic': Fore.MAGENTA,
        'plant': Fore.GREEN,
        'mushroom': Fore.RED,
        'enemy': Fore.RED + Style.BRIGHT,
        'npc': Fore.CYAN + Style.BRIGHT,
        'health': Fore.RED,
        'mana': Fore.BLUE,
        'xp': Fore.YELLOW,
        'item': Fore.GREEN,
        'location': Fore.CYAN,
        'quest': Fore.YELLOW + Style.BRIGHT,
    }

    # Gameplay settings
    STARTING_HEALTH = 100
    STARTING_MANA = 50
    STARTING_LEVEL = 1
    XP_MULTIPLIER = 1.5
    LEVEL_UP_XP = 100

    # Combat settings
    BASE_DAMAGE = 10
    CRIT_CHANCE = 0.1
    DODGE_CHANCE = 0.15

    # Inventory
    MAX_INVENTORY_SIZE = 20
    MAX_EQUIPPED_ITEMS = 5

    # Map settings
    MAP_WIDTH = 5
    MAP_HEIGHT = 5
    LOCATIONS_PER_AREA = 4

    # Save system
    SAVE_KEY = "MYCONAUT_SECRET_2024"
    SAVE_DIR = "saves"

    # Special effects
    HALLUCINATION_CHANCE = 0.3
    DISCOVERY_CHANCE = 0.25

    @classmethod
    def print_colored(cls, text, color_type='normal', end='\n'):
        """Print colored text with optional end parameter"""
        color = cls.COLORS.get(color_type, Fore.WHITE)
        print(color + text + Style.RESET_ALL, end=end)

    @classmethod
    def clear_screen(cls):
        """Clear terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')

    @classmethod
    def beep(cls, times=1):
        """Play system beep"""
        for _ in range(times):
            print('\a', end='', flush=True)
