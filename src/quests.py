"""
Myconaut - Quest System
"""

from ascii_art import ASCIIArt
from config import Config
from src.entities.item import create_item
from enum import Enum

class QuestStatus(Enum):
    """Quest status"""
    AVAILABLE = "available"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"

class QuestType(Enum):
    """Types of quests"""
    GATHER = "gather"
    KILL = "kill"
    DELIVER = "deliver"
    DISCOVER = "discover"
    CRAFT = "craft"

class Quest:
    """Quest class"""

    def __init__(self, id, name, description, quest_type, requirements, rewards,
                 giver_npc=None, target_npc=None, location=None, min_level=1):
        self.id = id
        self.name = name
        self.description = description
        self.type = quest_type
        self.requirements = requirements  # Dict with requirements
        self.rewards = rewards  # Dict with rewards
        self.giver_npc = giver_npc
        self.target_npc = target_npc
        self.location = location
        self.min_level = min_level
        self.status = QuestStatus.AVAILABLE
        self.progress = {}

    def can_start(self, player):
        """Check if player can start this quest"""
        if self.status != QuestStatus.AVAILABLE:
            return False

        if player.level < self.min_level:
            return False

        # Check if already completed
        if self.id in player.completed_quests:
            return False

        # Check location requirements
        if self.location and self.location not in player.visited_locations:
            return False

        return True

    def start(self, player):
        """Start the quest"""
        if not self.can_start(player):
            return False

        self.status = QuestStatus.ACTIVE
        player.active_quests.append(self.id)

        # Initialize progress based on quest type
        if self.type == QuestType.GATHER:
            items_needed = self.requirements.get('items', {})
            for item_id, needed in items_needed.items():
                # Check how many player already has
                current = 0
                if item_id in player.inventory.items:
                    current = min(player.inventory.items[item_id].quantity, needed)
                self.progress[item_id] = current

        elif self.type == QuestType.KILL:
            enemies_needed = self.requirements.get('enemies', {})
            for enemy_id, needed in enemies_needed.items():
                self.progress[enemy_id] = 0

        elif self.type == QuestType.DISCOVER:
            locations_needed = self.requirements.get('locations', [])
            for loc in locations_needed:
                self.progress[str(loc)] = loc in player.visited_locations

        elif self.type == QuestType.CRAFT:
            craft_item = self.requirements.get('craft', '')
            self.progress[craft_item] = False

        Config.print_colored(f"\nQuest started: {self.name}", 'quest')
        Config.print_colored(f"Objective: {self.description}", 'normal')
        Config.beep(2)
        return True

    def update_progress(self, player, update_type, target_id, amount=1):
        """Update quest progress"""
        if self.status != QuestStatus.ACTIVE:
            return False

        updated = False

        if self.type == QuestType.GATHER and update_type == "gather":
            if target_id in self.progress:
                current = self.progress[target_id]
                needed = self.requirements['items'][target_id]

                # Add to progress, but don't exceed needed amount
                new_progress = min(needed, current + amount)
                if new_progress > current:
                    self.progress[target_id] = new_progress
                    updated = True

                    # Check if item requirement is now met
                    if new_progress >= needed:
                        Config.print_colored(f"\nYou have collected enough {target_id.replace('_', ' ')} for the quest!", 'success')

        elif self.type == QuestType.KILL and update_type == "kill":
            if target_id in self.progress:
                current = self.progress[target_id]
                needed = self.requirements['enemies'][target_id]

                new_progress = min(needed, current + amount)
                if new_progress > current:
                    self.progress[target_id] = new_progress
                    updated = True

                    if new_progress >= needed:
                        Config.print_colored(f"\nYou have defeated enough {target_id.replace('_', ' ')} for the quest!", 'success')

        elif self.type == QuestType.DISCOVER and update_type == "discover":
            loc_str = str(target_id)
            if loc_str in self.progress and not self.progress[loc_str]:
                self.progress[loc_str] = True
                updated = True
                Config.print_colored(f"\nYou discovered a location needed for your quest!", 'success')

        elif self.type == QuestType.CRAFT and update_type == "craft":
            craft_item = self.requirements.get('craft', '')
            if target_id == craft_item and not self.progress[craft_item]:
                self.progress[craft_item] = True
                updated = True
                Config.print_colored(f"\nYou crafted the required item for your quest!", 'success')

        if updated:
            self.check_completion(player)

        return updated

    def check_completion(self, player):
        """Check if quest is complete"""
        if self.status != QuestStatus.ACTIVE:
            return False

        completed = False

        if self.type == QuestType.GATHER:
            items_needed = self.requirements.get('items', {})
            completed = all(
                self.progress.get(item_id, 0) >= needed
                for item_id, needed in items_needed.items()
            )

        elif self.type == QuestType.KILL:
            enemies_needed = self.requirements.get('enemies', {})
            completed = all(
                self.progress.get(enemy_id, 0) >= needed
                for enemy_id, needed in enemies_needed.items()
            )

        elif self.type == QuestType.DISCOVER:
            locations_needed = self.requirements.get('locations', [])
            completed = all(
                self.progress.get(str(loc), False)
                for loc in locations_needed
            )

        elif self.type == QuestType.CRAFT:
            craft_item = self.requirements.get('craft', '')
            completed = self.progress.get(craft_item, False)

        if completed:
            self.complete(player)
            return True

        return False

    def complete(self, player):
        """Complete the quest"""
        if self.status == QuestStatus.ACTIVE:
            self.status = QuestStatus.COMPLETED

            # Remove from active quests
            if self.id in player.active_quests:
                player.active_quests.remove(self.id)

            # Add to completed quests
            player.completed_quests.append(self.id)

            # Update story progress
            player.story_progress += 1

            # Give rewards
            Config.clear_screen()
            Config.print_colored(ASCIIArt.create_box("QUEST COMPLETED!"), 'quest')
            Config.print_colored(f"\n{self.name}", 'title')
            Config.print_colored(f"\n{self.description}\n", 'normal')

            reward_text = "Rewards:"

            if 'xp' in self.rewards:
                player.add_xp(self.rewards['xp'])
                reward_text += f" {self.rewards['xp']} XP,"

            if 'items' in self.rewards:
                for item_id in self.rewards['items']:
                    item = create_item(item_id)
                    if item:
                        player.inventory.add_item(item)
                        reward_text += f" {item.name},"

            if 'recipe' in self.rewards:
                player.add_recipe(self.rewards['recipe'])
                recipe_name = self.rewards['recipe'].replace('_', ' ').title()
                reward_text += f" {recipe_name} Recipe,"

            if 'ability' in self.rewards:
                # Add new ability
                reward_text += f" New Ability,"

            # Remove trailing comma
            if reward_text.endswith(','):
                reward_text = reward_text[:-1]

            Config.print_colored(f"\n{reward_text}", 'success')

            Config.beep(3)
            input("\nPress Enter to continue...")

            return True
        return False

# Quest definitions
QUESTS = {
    "welcome_to_myconaut": Quest(
        id="welcome_to_myconaut",
        name="Welcome to Myconaut",
        description="Collect 3 Glowing Moss samples from the forest",
        quest_type=QuestType.GATHER,
        requirements={
            'items': {'glowing_moss': 3}
        },
        rewards={
            'xp': 50,
            'items': ['healing_shroom', 'healing_shroom', 'mana_cap'],
            'recipe': 'health_potion_recipe'
        },
        giver_npc="elder_myconid",
        min_level=1
    ),

    "sporefang_menace": Quest(
        id="sporefang_menace",
        name="Sporefang Menace",
        description="Defeat 5 Sporefang enemies in the Murky Swamp",
        quest_type=QuestType.KILL,
        requirements={
            'enemies': {'sporefang': 5}
        },
        rewards={
            'xp': 100,
            'items': ['mana_cap', 'mana_cap', 'nightshade'],
            'recipe': 'mana_elixir_recipe'
        },
        giver_npc="elder_myconid",
        location=(2, 3),  # Murky Swamp
        min_level=2
    ),

    "lost_laboratory": Quest(
        id="lost_laboratory",
        name="The Lost Laboratory",
        description="Find the Ancient Laboratory in the northern forest",
        quest_type=QuestType.DISCOVER,
        requirements={
            'locations': [(3, 1)]  # Laboratory coordinates
        },
        rewards={
            'xp': 150,
            'items': ['forest_key'],
            'recipe': 'vision_potion_recipe'
        },
        giver_npc="elder_myconid",
        min_level=2
    ),

    "balance_tincture": Quest(
        id="balance_tincture",
        name="Brew of Balance",
        description="Craft a Balance Tincture to prove your alchemical skills",
        quest_type=QuestType.CRAFT,
        requirements={
            'craft': 'balance_tincture'
        },
        rewards={
            'xp': 200,
            'items': ['sun_blossom', 'sun_blossom', 'sun_blossom'],
            'recipe': 'forest_key_recipe'
        },
        giver_npc="elder_myconid",
        min_level=3
    ),

    "root_horror": Quest(
        id="root_horror",
        name="The Root Horror",
        description="Defeat the terrifying Root Horror in its lair",
        quest_type=QuestType.KILL,
        requirements={
            'enemies': {'root_horror': 1}
        },
        rewards={
            'xp': 500,
            'items': ['cave_key', 'balance_tincture', 'vision_fungus', 'vision_fungus'],
            'recipe': 'cave_key_recipe'
        },
        giver_npc="corrupted_druid",
        location=(0, 2),  # Boss room
        min_level=5
    ),

    "fungal_knowledge": Quest(
        id="fungal_knowledge",
        name="Fungal Knowledge",
        description="Collect 2 of each: Healing Shroom, Mana Cap, and Vision Fungus",
        quest_type=QuestType.GATHER,
        requirements={
            'items': {
                'healing_shroom': 2,
                'mana_cap': 2,
                'vision_fungus': 2
            }
        },
        rewards={
            'xp': 150,
            'items': ['health_potion', 'mana_elixir', 'health_potion'],
            'recipe': 'cave_key_recipe'
        },
        giver_npc="forest_ghost",
        min_level=3
    )
}

class QuestManager:
    """Manages player quests"""

    def __init__(self, player):
        self.player = player
        self.quests = QUESTS.copy()

    def get_available_quests(self):
        """Get quests available to player"""
        available = []

        for quest_id, quest in self.quests.items():
            if quest.can_start(self.player):
                available.append(quest)

        return available

    def get_active_quests(self):
        """Get player's active quests"""
        active = []

        for quest_id in self.player.active_quests:
            if quest_id in self.quests:
                quest = self.quests[quest_id]
                if quest.status == QuestStatus.ACTIVE:
                    active.append(quest)

        return active

    def start_quest(self, quest_id):
        """Start a quest"""
        if quest_id in self.quests:
            quest = self.quests[quest_id]
            return quest.start(self.player)
        return False

    def update_quest(self, update_type, target_id, amount=1):
        """Update progress on all active quests"""
        updated = False

        for quest_id in self.player.active_quests:
            if quest_id in self.quests:
                quest = self.quests[quest_id]
                if quest.update_progress(self.player, update_type, target_id, amount):
                    updated = True

        return updated

    def display_quest_log(self):
        """Display quest log"""
        Config.clear_screen()

        Config.print_colored("\n╔══════════════════════════════════════════════════════════════════════╗", 'quest')
        Config.print_colored("║                             QUEST LOG                                ║", 'quest')
        Config.print_colored("╠══════════════════════════════════════════════════════════════════════╣", 'quest')

        # Active quests
        active_quests = self.get_active_quests()
        if active_quests:
            Config.print_colored("\nACTIVE QUESTS:", 'highlight')
            for quest in active_quests:
                Config.print_colored(f"\n  • {quest.name}", 'quest')
                Config.print_colored(f"    {quest.description}", 'normal')

                # Show progress
                if quest.type == QuestType.GATHER:
                    for item_id, needed in quest.requirements.get('items', {}).items():
                        current = quest.progress.get(item_id, 0)
                        item = create_item(item_id)
                        if item:
                            color = 'success' if current >= needed else 'normal'
                            Config.print_colored(f"    {item.name}: {current}/{needed}", color)

                elif quest.type == QuestType.KILL:
                    for enemy_id, needed in quest.requirements.get('enemies', {}).items():
                        current = quest.progress.get(enemy_id, 0)
                        enemy_name = enemy_id.replace('_', ' ').title()
                        color = 'success' if current >= needed else 'normal'
                        Config.print_colored(f"    {enemy_name}: {current}/{needed}", color)

                elif quest.type == QuestType.DISCOVER:
                    locations = quest.requirements.get('locations', [])
                    for loc in locations:
                        discovered = quest.progress.get(str(loc), False)
                        loc_name = "Unknown Location"
                        color = 'success' if discovered else 'normal'
                        Config.print_colored(f"    Location: {'Discovered' if discovered else 'Not Found'}", color)

                elif quest.type == QuestType.CRAFT:
                    craft_item = quest.requirements.get('craft', '')
                    crafted = quest.progress.get(craft_item, False)
                    item_name = craft_item.replace('_', ' ').title()
                    color = 'success' if crafted else 'normal'
                    Config.print_colored(f"    {item_name}: {'Crafted' if crafted else 'Not Crafted'}", color)

        else:
            Config.print_colored("\nNo active quests. Talk to NPCs to get quests.", 'info')

        # Available quests
        available_quests = self.get_available_quests()
        if available_quests:
            Config.print_colored("\nAVAILABLE QUESTS:", 'highlight')
            for quest in available_quests:
                Config.print_colored(f"  • {quest.name} (Level {quest.min_level}+)", 'quest')
                Config.print_colored(f"    {quest.description}", 'normal')

        # Completed quests
        if self.player.completed_quests:
            Config.print_colored("\nCOMPLETED QUESTS:", 'highlight')
            for quest_id in self.player.completed_quests:
                if quest_id in self.quests:
                    quest = self.quests[quest_id]
                    Config.print_colored(f"  ✓ {quest.name}", 'success')

        Config.print_colored("\n╚══════════════════════════════════════════════════════════════════════╝", 'quest')
        input("\nPress Enter to continue...")
