"""
Myconaut - Main Game Class
"""

import sys
import os
# Add parent directory to path for config import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from ascii_art import ASCIIArt
from player import Player
from world.location import get_location, LocationType
from quests import QuestManager
from alchemy import AlchemyStation
from combat import Combat
from entities.item import create_item
from entities.npc import get_npc
from save_system import SaveSystem
from systems.hallucination_system import HallucinationManager
import random
import time


class Game:
    """Main game controller"""

    def __init__(self):
        self.player = None
        self.quest_manager = None
        self.alchemy_station = None
        self.save_system = SaveSystem()
        self.hallucination_manager = HallucinationManager()
        self.game_running = False
        self.current_turn = 0
        self.game_start_time = None

    def start_new_game(self):
        """Start a new game"""
        Config.clear_screen()
        print(ASCIIArt.title_screen())

        # Get player name
        Config.print_colored("\nWhat is your name, traveler?", 'info')
        name = input("> ").strip()

        if not name:
            name = "Myconaut"

        # Create player
        self.player = Player(name)
        self.quest_manager = QuestManager(self.player)
        self.alchemy_station = AlchemyStation(self.player)

        # Give starting items
        self.player.inventory.add_item(create_item("healing_shroom"), 3)
        self.player.inventory.add_item(create_item("glowing_moss"), 2)
        self.player.inventory.add_item(create_item("mana_cap"), 2)

        # Add starting recipe
        self.player.add_recipe("health_potion_recipe")

        # Game state
        self.game_running = True
        self.game_start_time = time.time()
        self.current_turn = 0

        Config.print_colored(f"\nWelcome, {name}! Your journey begins...", 'title')
        Config.beep()
        time.sleep(2)

        # Start at forest clearing
        self.enter_location(2, 2)

    def main_loop(self):
        """Main game loop"""
        while self.game_running and self.player.health > 0:
            self.current_turn += 1

            # Update hallucinations
            self.hallucination_manager.update(self)

            # Check for random events
            self.check_random_events()

            # Regenerate mana every 5 turns
            if self.current_turn % 5 == 0 and self.player.mana < self.player.max_mana:
                self.player.restore_mana(5)
                Config.print_colored("Your mana regenerates slightly...", 'mana')

            # Display location and get player action
            location = get_location(*self.player.current_location)
            if location:
                location.display()
                self.location_menu(location)
            else:
                Config.print_colored("You are lost in the void...", 'error')
                break

        if self.player.health <= 0:
            self.game_over()

    def location_menu(self, location):
        """Display location menu and handle actions"""
        while True:
            options = []

            # Movement options
            available_directions = location.get_available_directions()
            for direction_code, direction_name in available_directions:
                options.append((direction_code.upper(), f"Go {direction_name}", f"Travel {direction_name}"))

            # Location-specific options
            options.append(("X", "eXplore", "Search for items in this area"))

            if location.has_enemies():
                options.append(("F", "Fight", "Engage enemies in combat"))

            if location.npcs:
                options.append(("T", "Talk", "Speak with someone here"))

            # General options
            options.append(("I", "Inventory", "View your inventory"))
            options.append(("C", "Character", "View your character stats"))
            options.append(("Q", "Quests", "View your quest log"))
            options.append(("A", "Alchemy", "Access alchemy menu"))
            options.append(("R", "cRaft", "Craft items at camp"))
            options.append(("M", "Map", "View world map"))
            options.append(("V", "saVe", "Save your game"))
            options.append(("H", "Help", "Show available commands"))
            options.append(("L", "Leave", "Exit to main menu"))

            # Display menu
            Config.print_colored("\nWhat would you like to do?", 'highlight')

            for key, action, desc in options:
                display_text = f"  [{key}] {action:12} - {desc}"

                # Apply hallucination effects to text
                if self.hallucination_manager.active_effects:
                    display_text = self.hallucination_manager.modify_output(display_text)

                print(display_text)

            raw_choice = input("\nChoose action: ").strip().upper()

            # Handle choice
            if raw_choice.lower() in [d[0].lower() for d in available_directions]:
                self.move_player(raw_choice.lower())
                break
            elif raw_choice == "X":
                self.explore_location(location)
            elif raw_choice == "F":
                if location.has_enemies():
                    self.start_combat(location)
                break
            elif raw_choice == "T":
                if location.npcs:
                    self.talk_to_npc(location)
            elif raw_choice == "I":
                self.player.inventory.display()
                input("\nPress Enter to continue...")
            elif raw_choice == "C":
                self.player.display_stats()
                input("\nPress Enter to continue...")
            elif raw_choice == "Q":
                self.quest_manager.display_quest_log()
            elif raw_choice == "A":
                self.alchemy_station.display()
            elif raw_choice == "R":
                self.craft_at_camp()
            elif raw_choice == "M":
                self.display_map()
            elif raw_choice == "V":
                self.save_game()
            elif raw_choice == "H":
                self.show_commands_help()
            elif raw_choice == "L":
                self.return_to_menu()
                break
            else:
                Config.print_colored("Invalid choice! Type 'H' for help.", 'error')

    def move_player(self, direction):
        """Move player to new location"""
        current_loc = get_location(*self.player.current_location)

        if not current_loc or direction not in current_loc.connections:
            Config.print_colored("You can't go that way!", 'error')
            return

        new_coords = current_loc.connections[direction]
        new_location = get_location(*new_coords)

        if not new_location:
            Config.print_colored("That area is inaccessible!", 'error')
            return

        # Check if location requires key
        if new_location.requires_key and new_location.key_item:
            if not self.player.inventory.has_item(new_location.key_item):
                Config.print_colored(f"This area is locked! You need a {new_location.key_item.replace('_', ' ')}.", 'warning')
                return

        # Update player position
        self.player.current_location = new_coords
        self.player.visited_locations.add(new_coords)

        # 30% chance of random encounter when moving
        if not new_location.is_safe and random.random() < 0.3:
            self.random_encounter(new_location)

        # Enter new location
        self.enter_location(*new_coords)

    def random_encounter(self, location):
        """Random encounter while moving"""
        encounter_chance = random.random()

        if encounter_chance < 0.6:  # 60% chance of enemy
            enemies = ["sporefang", "fungal_ooze", "sporefang", "fungal_ooze"]
            if location.type.value in ["cave", "swamp"]:
                enemies = ["sporefang", "mindshroom", "thornbeast"]

            enemy_id = random.choice(enemies)
            Config.print_colored(f"\nWhile moving, you encounter a {enemy_id.replace('_', ' ')}!", 'enemy')
            time.sleep(1)

            combat = Combat(self.player, enemy_id)
            combat.start()

            if not combat.enemy.is_alive():
                self.quest_manager.update_quest("kill", enemy_id)

        elif encounter_chance < 0.8:  # 20% chance of finding item
            items = ["glowing_moss", "healing_shroom", "mana_cap"]
            item_id = random.choice(items)
            item = create_item(item_id)
            if item:
                self.player.inventory.add_item(item)
                Config.print_colored(f"\nYou stumble upon a {item.name}!", 'item')

        else:  # 20% chance of hallucination
            self.hallucination_manager.add_effect("visual_distortion")
            Config.print_colored("\nThe world shifts strangely around you...", 'magic')

        time.sleep(1.5)

    def enter_location(self, x, y):
        """Enter a location"""
        location = get_location(x, y)

        if not location:
            return

        # Mark as discovered for quests
        self.quest_manager.update_quest("discover", (x, y))

        # Special location effects
        if location.type == LocationType.LABORATORY and not self.player.found_laboratory:
            self.player.found_laboratory = True
            Config.print_colored("You discover an ancient alchemy laboratory!", 'success')
            self.player.add_recipe("vision_potion_recipe")
            self.player.add_recipe("balance_tincture_recipe")

        elif location.type == LocationType.VILLAGE and not self.player.has_met_elder:
            self.player.has_met_elder = True
            self.player.story_progress = 1
            # Start first quest automatically
            if "welcome_to_myconaut" not in self.player.completed_quests:
                self.quest_manager.start_quest("welcome_to_myconaut")
                Config.print_colored("\nThe Elder Myconid has a quest for you!", 'quest')

        elif location.type == LocationType.BOSS_ROOM:
            Config.print_colored("A terrifying presence fills the air...", 'error')
            Config.beep(3)

        elif location.type == LocationType.ALTAR:
            Config.print_colored("You feel a sense of peace and balance here.", 'success')
            # Heal at altar
            self.player.heal(self.player.max_health // 2)
            self.player.restore_mana(self.player.max_mana // 2)

    def explore_location(self, location):
        """Explore current location for items"""
        found_items = location.explore()

        if found_items:
            Config.print_colored("\nYou search the area and find:", 'success')
            for item_id in found_items:
                item = create_item(item_id)
                if item:
                    self.player.inventory.add_item(item)

            # Update gather quests
            for item_id in found_items:
                self.quest_manager.update_quest("gather", item_id, 1)
        else:
            Config.print_colored("\nYou don't find anything of value.", 'info')

        # 25% chance to encounter enemy while exploring
        if not location.is_safe and random.random() < 0.25:
            Config.print_colored("\nWhile exploring, you disturb something...", 'warning')
            time.sleep(1)
            enemy_id = location.get_random_enemy()
            if enemy_id:
                combat = Combat(self.player, enemy_id)
                combat.start()
                if not combat.enemy.is_alive():
                    self.quest_manager.update_quest("kill", enemy_id)

        input("\nPress Enter to continue...")

    def start_combat(self, location):
        """Start combat with random enemy"""
        enemy_id = location.get_random_enemy()

        if not enemy_id:
            Config.print_colored("No enemies found!", 'info')
            return

        combat = Combat(self.player, enemy_id)
        combat.start()

        # Update kill quests
        if not combat.enemy.is_alive():
            self.quest_manager.update_quest("kill", enemy_id)

        # Heal a bit after combat
        if self.player.health > 0:
            heal_amount = self.player.max_health // 10
            self.player.heal(heal_amount)
            Config.print_colored(f"\nYou catch your breath and recover {heal_amount} HP.", 'health')

    def talk_to_npc(self, location):
        """Talk to NPC in location"""
        if not location.npcs:
            Config.print_colored("There's no one here to talk to.", 'info')
            input("\nPress Enter to continue...")
            return

        # For now, talk to the first NPC
        npc_id = location.npcs[0]
        npc = get_npc(npc_id)

        if npc:
            result = npc.talk(self.player)

            # Handle conversation result
            if result == "start_quest":
                # Start appropriate quest based on NPC
                if npc.id == "elder_myconid":
                    if "welcome_to_myconaut" in self.player.completed_quests:
                        if "sporefang_menace" not in self.player.completed_quests:
                            self.quest_manager.start_quest("sporefang_menace")
                        elif "lost_laboratory" not in self.player.completed_quests:
                            self.quest_manager.start_quest("lost_laboratory")
                        elif "balance_tincture" not in self.player.completed_quests:
                            self.quest_manager.start_quest("balance_tincture")
                    elif not self.player.has_met_elder:
                        # Start first quest
                        self.quest_manager.start_quest("welcome_to_myconaut")
                        self.player.has_met_elder = True
                        self.player.story_progress = 1
                        Config.beep(2)

            elif result == "complete_quest":
                # Complete current quest
                pass

            elif result == "trade":
                # Trading not implemented yet
                Config.print_colored("Trading is not available yet.", 'info')
                input("\nPress Enter to continue...")

            # No need for additional input here - the NPC.talk method handles everything

    def craft_at_camp(self):
        """Craft items at campsite"""
        Config.print_colored("\nYou set up a temporary camp and prepare to craft...", 'info')

        # Check if player knows any recipes
        if not self.player.discovered_recipes:
            Config.print_colored("You don't know any recipes yet. Learn some from NPCs or by experimenting.", 'warning')
            input("\nPress Enter to continue...")
            return

        # Show known recipes
        self.alchemy_station.view_recipes()

        # Ask if they want to craft
        Config.print_colored("\nWould you like to craft something from your known recipes? (Y/N)", 'info')
        choice = input("> ").strip().upper()

        if choice == "Y":
            self.alchemy_station.craft_item()

    def display_map(self):
        """Display world map"""
        Config.clear_screen()

        Config.print_colored("\n╔══════════════════════════════════════════════════════════════════════╗", 'location')
        Config.print_colored("║                             WORLD MAP                                ║", 'location')
        Config.print_colored("╠══════════════════════════════════════════════════════════════════════╣", 'location')

        map_grid = [
            ["   ", "   ", "Alt", "   ", "   "],
            ["   ", "   ", "Vil", "Lab", "   "],
            ["Mtn", "   ", "For", "Cav", "   "],
            ["   ", "   ", "Swp", "Gro", "   "],
            ["   ", "   ", "   ", "   ", "   "]
        ]

        # Add player marker
        px, py = self.player.current_location
        if 0 <= px < 5 and 0 <= py < 5:
            map_grid[py][px] = "YOU"

        Config.print_colored("\n          N", 'info')
        Config.print_colored("          ↑", 'info')

        for y, row in enumerate(map_grid):
            line = "    "
            for x, cell in enumerate(row):
                if cell == "YOU":
                    line += Config.COLORS['title'] + "[YOU]" + Config.COLORS['normal']
                elif cell.strip():
                    # Add color based on location type
                    color = Config.COLORS['location']
                    if cell == "For":
                        color = Config.COLORS['plant']
                    elif cell == "Cav":
                        color = Config.COLORS['info']
                    elif cell == "Vil":
                        color = Config.COLORS['npc']
                    elif cell == "Swp":
                        color = Config.COLORS['mushroom']
                    elif cell == "Mtn":
                        color = Config.COLORS['highlight']
                    elif cell == "Alt":
                        color = Config.COLORS['magic']
                    elif cell == "Lab":
                        color = Config.COLORS['quest']
                    elif cell == "Gro":
                        color = Config.COLORS['enemy']

                    line += color + f"[{cell:^3}]" + Config.COLORS['normal']
                else:
                    line += "[   ]"

            # Add compass indicator
            if y == 2:
                line += "  W ←   → E"

            print(line)

        Config.print_colored("          ↓", 'info')
        Config.print_colored("          S", 'info')

        Config.print_colored("\n╠══════════════════════════════════════════════════════════════════════╣", 'location')
        Config.print_colored("║ Legend:                                                              ║", 'location')
        Config.print_colored("║   [YOU] - Your location    [For] - Forest     [Cav] - Cave           ║", 'location')
        Config.print_colored("║   [Vil] - Village          [Swp] - Swamp      [Mtn] - Mountain       ║", 'location')
        Config.print_colored("║   [Lab] - Laboratory       [Gro] - Grove      [Alt] - Altar          ║", 'location')
        Config.print_colored("╚══════════════════════════════════════════════════════════════════════╝", 'location')

        # Show player position
        x, y = self.player.current_location
        Config.print_colored(f"\nYour position: ({x}, {y})", 'info')

        input("\nPress Enter to continue...")

    def save_game(self):
        """Save current game"""
        password = self.save_system.save_game(self.player, self)
        if password:
            input("\nPress Enter to continue...")

    def load_game(self, password):
        """Load game from password"""
        player_data, game_data = self.save_system.load_game(password)

        if not player_data:
            Config.print_colored("Failed to load game!", 'error')
            return False

        # Create new player and load data
        self.player = Player(player_data['name'])
        self.player.load_data(player_data)

        # Recreate managers
        self.quest_manager = QuestManager(self.player)
        self.alchemy_station = AlchemyStation(self.player)

        # Load game data
        if game_data:
            self.current_turn = game_data.get('current_turn', 0)

        self.game_running = True

        Config.print_colored("Game loaded successfully!", 'success')
        Config.beep()
        time.sleep(1)

        # Enter current location
        self.enter_location(*self.player.current_location)

        return True

    def check_random_events(self):
        """Check for random events"""
        # Chance for hallucination from consumed substances
        if "vision" in self.player.hallucinations and random.random() < 0.2:
            self.hallucination_manager.add_effect("visual_distortion")

        # Chance to find random item (lower chance)
        if random.random() < 0.02:  # 2% chance per turn
            random_items = ["glowing_moss", "healing_shroom", "mana_cap"]
            item_id = random.choice(random_items)
            item = create_item(item_id)
            if item:
                self.player.inventory.add_item(item)
                Config.print_colored(f"You randomly find a {item.name}!", 'item')

        # Chance for weather/atmosphere effects
        if random.random() < 0.1:
            effects = [
                "A gentle breeze rustles the leaves...",
                "Strange spores drift through the air...",
                "You hear distant whispers in the wind...",
                "The ground beneath you feels alive..."
            ]
            Config.print_colored(f"\n{random.choice(effects)}", 'info')

    def game_over(self):
        """Handle game over"""
        Config.clear_screen()

        Config.print_colored(ASCIIArt.create_box("GAME OVER"), 'error')
        Config.print_colored("\nYour journey ends here...", 'error')

        play_time = time.time() - self.game_start_time if self.game_start_time else 0
        hours, remainder = divmod(int(play_time), 3600)
        minutes, seconds = divmod(remainder, 60)

        Config.print_colored(f"\nYou survived for: {hours:02d}:{minutes:02d}:{seconds:02d}", 'info')
        Config.print_colored(f"Level reached: {self.player.level}", 'info')
        Config.print_colored(f"Quests completed: {len(self.player.completed_quests)}", 'info')
        Config.print_colored(f"Locations discovered: {len(self.player.visited_locations)}", 'info')

        Config.print_colored("\n\nThank you for playing Myconaut!", 'title')
        Config.print_colored("Remember: Balance is key in all things.", 'highlight')

        Config.beep(2)
        input("\nPress Enter to return to main menu...")

        self.return_to_menu()

    def return_to_menu(self):
        """Return to main menu"""
        self.game_running = False

    def show_commands_help(self):
        """Show help for available commands"""
        Config.clear_screen()
        Config.print_colored(ASCIIArt.create_box("AVAILABLE COMMANDS"), 'title')

        help_text = """
    MOVEMENT:
        N, n, North      - Go north
        S, s, South      - Go south
        E, e, East       - Go east
        W, w, West       - Go west

    ACTIONS:
        X, x             - eXplore current location
        F, f             - Fight enemies (if present)
        T, t             - Talk to NPCs (if present)

    MENUS:
        I, i             - Inventory
        C, c             - Character stats
        Q, q             - Quest log
        A, a             - ALchemy station
        R, r             - cRaft items
        M, m             - Map (world)
        V, v             - saVe game
        H, h             - Help (show this)
        L, l             - Leave to main menu

    COMBAT CONTROLS:
        1                - Basic attack
        2                - Use ability
        3                - Use item
        4                - Attempt escape

    GENERAL:
        • All letters are case-insensitive
        • Press Enter to confirm
        • Type 'H' anytime for help
        • Movement uses standard compass directions
        • Some actions may trigger random events
        """

        print(Config.COLORS['normal'] + help_text)
        input("\nPress Enter to continue...")

    def save_data(self):
        """Prepare game data for saving"""
        return {
            'current_turn': self.current_turn,
            'game_start_time': self.game_start_time
        }
