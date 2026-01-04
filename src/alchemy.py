"""
Myconaut - Alchemy System
"""

from config import Config
from src.ascii_art import ASCIIArt
from src.entities.item import create_item, ItemType
import random

class Recipe:
    """Alchemy recipe"""

    def __init__(self, id, name, description, ingredients, result, required_level=1):
        self.id = id
        self.name = name
        self.description = description
        self.ingredients = ingredients  # List of (item_id, quantity)
        self.result = result  # item_id
        self.required_level = required_level

    def can_craft(self, player):
        """Check if player can craft this recipe"""
        # Check level
        if player.level < self.required_level:
            return False

        # Check ingredients
        for item_id, quantity in self.ingredients:
            if not player.inventory.has_item(item_id, quantity):
                return False

        return True

    def craft(self, player):
        """Craft the recipe"""
        if not self.can_craft(player):
            return None

        # Remove ingredients
        for item_id, quantity in self.ingredients:
            player.inventory.remove_item(item_id, quantity)

        # Create result item
        result_item = create_item(self.result)
        if result_item:
            player.inventory.add_item(result_item)

        # Discovery chance
        if random.random() < Config.DISCOVERY_CHANCE and self.id not in player.discovered_recipes:
            player.add_recipe(self.id)

        return result_item

# Alchemy recipes
RECIPES = {
    # Basic recipes
    "health_potion_recipe": Recipe(
        id="health_potion_recipe",
        name="Health Potion Recipe",
        description="Craft a basic healing potion",
        ingredients=[("healing_shroom", 2), ("glowing_moss", 1)],
        result="health_potion",
        required_level=1
    ),

    "mana_elixir_recipe": Recipe(
        id="mana_elixir_recipe",
        name="Mana Elixir Recipe",
        description="Craft a mana restoration elixir",
        ingredients=[("mana_cap", 2), ("glowing_moss", 2)],
        result="mana_elixir",
        required_level=2
    ),

    # Advanced recipes
    "vision_potion_recipe": Recipe(
        id="vision_potion_recipe",
        name="Vision Potion Recipe",
        description="Craft a potion that grants psychic visions",
        ingredients=[("vision_fungus", 1), ("nightshade", 1), ("mana_cap", 1)],
        result="vision_potion",
        required_level=3
    ),

    "balance_tincture_recipe": Recipe(
        id="balance_tincture_recipe",
        name="Balance Tincture Recipe",
        description="Craft a tincture that restores balance",
        ingredients=[("sun_blossom", 1), ("healing_shroom", 1), ("mana_cap", 1)],
        result="balance_tincture",
        required_level=4
    ),

    # Key recipes
    "forest_key_recipe": Recipe(
        id="forest_key_recipe",
        name="Forest Key Recipe",
        description="Craft a key to unlock the ancient laboratory",
        ingredients=[("nightshade", 3), ("sun_blossom", 2), ("vision_fungus", 1)],
        result="forest_key",
        required_level=5
    ),

    "cave_key_recipe": Recipe(
        id="cave_key_recipe",
        name="Crystal Key Recipe",
        description="Craft a key to unlock the crystal caverns",
        ingredients=[("glowing_moss", 3), ("mana_cap", 2), ("healing_shroom", 2)],
        result="cave_key",
        required_level=5
    ),
}

class AlchemyStation:
    """Alchemy crafting interface"""

    def __init__(self, player):
        self.player = player

    def display(self):
        """Display alchemy interface"""
        Config.clear_screen()
        Config.print_colored(ASCIIArt.create_box("ALCHEMY LABORATORY"), 'title')
        Config.print_colored("\nYou stand before an alchemy station. What would you like to do?\n", 'info')

        while True:
            options = [
                ("1", "View Recipes", "See all known recipes"),
                ("2", "Craft Item", "Craft an item from a recipe"),
                ("3", "Experiment", "Try to discover new recipes (costs materials)"),
                ("4", "Return", "Leave the alchemy station")
            ]

            for key, action, desc in options:
                Config.print_colored(f"  [{key}] {action:15} - {desc}", 'normal')

            choice = input("\nChoose action: ").strip()

            if choice == "1":
                self.view_recipes()
            elif choice == "2":
                self.craft_item()
            elif choice == "3":
                self.experiment()
            elif choice == "4":
                Config.print_colored("You leave the alchemy station.", 'info')
                break
            else:
                Config.print_colored("Invalid choice!", 'error')

    def view_recipes(self):
        """View known recipes"""
        Config.clear_screen()

        if not self.player.discovered_recipes:
            Config.print_colored("You haven't discovered any recipes yet!", 'warning')
            input("\nPress Enter to continue...")
            return

        Config.print_colored("\n╔══════════════════════════════════════════════════════════════════════╗", 'highlight')
        Config.print_colored("║                          KNOWN RECIPES                               ║", 'highlight')
        Config.print_colored("╠══════════════════════════════════════════════════════════════════════╣", 'highlight')

        for idx, recipe_id in enumerate(self.player.discovered_recipes, 1):
            recipe = RECIPES.get(recipe_id)
            if recipe:
                Config.print_colored(f"\n  [{idx}] {recipe.name}", 'quest')
                Config.print_colored(f"      {recipe.description}", 'normal')

                # Show ingredients
                Config.print_colored("      Ingredients:", 'info')
                for item_id, quantity in recipe.ingredients:
                    item = create_item(item_id)
                    if item:
                        has_item = self.player.inventory.has_item(item_id, quantity)
                        color = 'success' if has_item else 'warning'
                        Config.print_colored(f"        • {quantity}x {item.name}", color)

                # Show result
                result_item = create_item(recipe.result)
                if result_item:
                    Config.print_colored(f"      Result: {result_item.name}", 'item')

        Config.print_colored("\n╚══════════════════════════════════════════════════════════════════════╝", 'highlight')
        input("\nPress Enter to continue...")

    def craft_item(self):
        """Craft an item"""
        if not self.player.discovered_recipes:
            Config.print_colored("You haven't discovered any recipes yet!", 'warning')
            return

        Config.clear_screen()
        Config.print_colored("\nSelect a recipe to craft:\n", 'info')

        # List available recipes
        available_recipes = []
        for recipe_id in self.player.discovered_recipes:
            recipe = RECIPES.get(recipe_id)
            if recipe and recipe.can_craft(self.player):
                available_recipes.append(recipe)

        if not available_recipes:
            Config.print_colored("You don't have the materials for any recipe!", 'warning')
            input("\nPress Enter to continue...")
            return

        for idx, recipe in enumerate(available_recipes, 1):
            Config.print_colored(f"  [{idx}] {recipe.name}", 'quest')

        try:
            choice = int(input("\nChoose recipe (0 to cancel): "))
            if choice == 0:
                return

            if 1 <= choice <= len(available_recipes):
                recipe = available_recipes[choice - 1]
                result = recipe.craft(self.player)

                if result:
                    Config.print_colored(f"\nYou successfully craft a {result.name}!", 'success')
                    Config.beep()
                else:
                    Config.print_colored("Crafting failed!", 'error')
            else:
                Config.print_colored("Invalid choice!", 'error')
        except ValueError:
            Config.print_colored("Invalid input!", 'error')

        input("\nPress Enter to continue...")

    def experiment(self):
        """Try to discover new recipes"""
        Config.clear_screen()
        Config.print_colored("\nYou attempt to experiment with your materials...\n", 'info')

        # Need at least 2 different types of items
        plant_items = self.player.inventory.get_items_by_type(ItemType.PLANT)
        mushroom_items = self.player.inventory.get_items_by_type(ItemType.MUSHROOM)

        if len(plant_items) < 1 or len(mushroom_items) < 1:
            Config.print_colored("You need both plants and mushrooms to experiment!", 'warning')
            input("\nPress Enter to continue...")
            return

        # Cost: 1 random plant and 1 random mushroom
        plant_item = random.choice(plant_items)
        mushroom_item = random.choice(mushroom_items)

        Config.print_colored(f"You use: {plant_item.name} and {mushroom_item.name}", 'normal')

        # Remove used items
        self.player.inventory.remove_item(plant_item.id, 1)
        self.player.inventory.remove_item(mushroom_item.id, 1)

        # Chance to discover recipe
        discovery_chance = 0.3 + (self.player.level * 0.05)

        if random.random() < discovery_chance:
            # Find an undiscovered recipe
            undiscovered = [r for r in RECIPES.keys() if r not in self.player.discovered_recipes]

            if undiscovered:
                discovered_recipe_id = random.choice(undiscovered)
                self.player.add_recipe(discovered_recipe_id)

                recipe = RECIPES[discovered_recipe_id]
                Config.print_colored(f"\nSuccess! You discover the {recipe.name}!", 'success')
                Config.beep(2)
            else:
                Config.print_colored("\nYou've already discovered all recipes!", 'info')
        else:
            Config.print_colored("\nThe experiment fails. The mixture turns to useless sludge.", 'warning')

        input("\nPress Enter to continue...")
