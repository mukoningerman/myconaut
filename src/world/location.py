"""
Myconaut - Location System
"""

from config import Config
from src.ascii_art import ASCIIArt
import random
from enum import Enum

class LocationType(Enum):
    """Types of locations"""
    FOREST = "forest"
    CAVE = "cave"
    VILLAGE = "village"
    SWAMP = "swamp"
    MOUNTAIN = "mountain"
    LABORATORY = "laboratory"
    ALTAR = "altar"
    BOSS_ROOM = "boss_room"

class Location:
    """Game location"""

    def __init__(self, name, location_type, description, ascii_art, connections=None,
                 enemies=None, items=None, npcs=None, is_safe=False, requires_key=False, key_item=None):
        self.name = name
        self.type = location_type
        self.description = description
        self.ascii_art = ascii_art
        self.connections = connections or {}  # direction: (x, y)
        self.enemies = enemies or []
        self.items = items or []
        self.npcs = npcs or []
        self.is_safe = is_safe
        self.requires_key = requires_key
        self.key_item = key_item
        self.visited = False
        self.explored_items = []
        self.respawn_timer = 0
        self.max_respawn_time = 10  # Turns until items respawn

    def display(self):
        """Display location information"""
        Config.clear_screen()

        # Show ASCII art for location
        if self.ascii_art:
            print(self.ascii_art())

        Config.print_colored(f"\n╔══════════════════════════════════════════════════════════════════════╗", 'location')
        Config.print_colored(f"║ {self.name:^74} ║", 'location')
        Config.print_colored(f"╚══════════════════════════════════════════════════════════════════════╝\n", 'location')

        Config.print_colored(f"{self.description}\n", 'normal')

        if not self.visited:
            Config.print_colored("You discover this location for the first time!", 'success')
            self.visited = True
            Config.beep(2)

        # Check if items have respawned
        if self.respawn_timer > 0:
            self.respawn_timer -= 1

        # Show available directions
        if self.connections:
            directions = []
            for direction in self.connections:
                if direction == 'n':
                    directions.append("North")
                elif direction == 's':
                    directions.append("South")
                elif direction == 'e':
                    directions.append("East")
                elif direction == 'w':
                    directions.append("West")

            if directions:
                Config.print_colored("Paths lead: " + ", ".join(directions), 'info')

        # Show items in location (if not explored or respawned)
        if self.items and (not self.explored_items or self.respawn_timer == 0):
            Config.print_colored("\nYou notice some resources here:", 'item')
            for item_id in self.items:
                item_name = item_id.replace('_', ' ').title()
                # Show different descriptions based on item type
                if "moss" in item_id:
                    Config.print_colored(f"  • {item_name} (glows softly)", 'item')
                elif "shroom" in item_id:
                    Config.print_colored(f"  • {item_name} (red cap)", 'item')
                elif "cap" in item_id:
                    Config.print_colored(f"  • {item_name} (blue mushroom)", 'item')
                elif "fungus" in item_id:
                    Config.print_colored(f"  • {item_name} (strange mushroom)", 'item')
                elif "blossom" in item_id:
                    Config.print_colored(f"  • {item_name} (bright flower)", 'item')
                elif "nightshade" in item_id:
                    Config.print_colored(f"  • {item_name} (purple flowers)", 'item')
                else:
                    Config.print_colored(f"  • {item_name}", 'item')

        elif self.respawn_timer > 0:
            Config.print_colored(f"\nResources will regrow in {self.respawn_timer} turns.", 'info')

        # Show NPCs
        if self.npcs:
            Config.print_colored("\nPeople here:", 'npc')
            for npc_id in self.npcs:
                npc_name = self.get_npc_name(npc_id)
                Config.print_colored(f"  • {npc_name}", 'npc')

        # Show enemies
        if self.enemies and not self.is_safe:
            Config.print_colored("\nDangers:", 'enemy')
            for enemy_id in self.enemies:
                enemy_name = enemy_id.replace('_', ' ').title()
                # Add descriptions for enemies
                if enemy_id == "sporefang":
                    Config.print_colored(f"  • {enemy_name} (fast, poisonous)", 'enemy')
                elif enemy_id == "thornbeast":
                    Config.print_colored(f"  • {enemy_name} (strong, slow)", 'enemy')
                elif enemy_id == "mindshroom":
                    Config.print_colored(f"  • {enemy_name} (psychic, mana-draining)", 'enemy')
                elif enemy_id == "root_horror":
                    Config.print_colored(f"  • {enemy_name} (BOSS - extremely dangerous)", 'error')
                else:
                    Config.print_colored(f"  • {enemy_name}", 'enemy')

        # Show if location is safe
        if self.is_safe:
            Config.print_colored("\nThis area is safe. You can rest here.", 'success')

    def get_npc_name(self, npc_id):
        """Get NPC name by ID"""
        npc_names = {
            "elder_myconid": "Elder Myconid (quest giver)",
            "corrupted_druid": "Corrupted Druid (dangerous)",
            "forest_ghost": "Forest Ghost (mysterious spirit)"
        }
        return npc_names.get(npc_id, npc_id.replace('_', ' ').title())

    def get_available_directions(self):
        """Get list of available directions"""
        available = []

        if 'n' in self.connections:
            available.append(('n', "North"))
        if 's' in self.connections:
            available.append(('s', "South"))
        if 'e' in self.connections:
            available.append(('e', "East"))
        if 'w' in self.connections:
            available.append(('w', "West"))

        return available

    def explore(self):
        """Explore location for items"""
        # Check if items have respawned
        if self.respawn_timer > 0:
            return []

        if not self.items:
            return []

        found_items = []
        for item_id in self.items:
            # Different items have different discovery chances
            discovery_chance = 0.8  # 80% base chance

            # Adjust chance based on item rarity
            if "vision_fungus" in item_id:
                discovery_chance = 0.5  # 50% for rare items
            elif "nightshade" in item_id:
                discovery_chance = 0.6  # 60%
            elif "sun_blossom" in item_id:
                discovery_chance = 0.7  # 70%

            if random.random() < discovery_chance:
                found_items.append(item_id)

        self.explored_items.extend(found_items)

        # Start respawn timer
        if found_items:
            self.respawn_timer = self.max_respawn_time

        return found_items

    def has_enemies(self):
        """Check if location has enemies"""
        return bool(self.enemies and not self.is_safe)

    def get_random_enemy(self):
        """Get a random enemy from location"""
        if self.enemies:
            # Weight enemies based on difficulty
            weighted_enemies = []
            for enemy_id in self.enemies:
                if enemy_id == "sporefang":
                    weighted_enemies.extend([enemy_id] * 5)  # Common
                elif enemy_id == "fungal_ooze":
                    weighted_enemies.extend([enemy_id] * 4)  # Common
                elif enemy_id == "mindshroom":
                    weighted_enemies.extend([enemy_id] * 3)  # Uncommon
                elif enemy_id == "thornbeast":
                    weighted_enemies.extend([enemy_id] * 2)  # Rare
                elif enemy_id == "root_horror":
                    weighted_enemies.extend([enemy_id] * 1)  # Very rare

            if weighted_enemies:
                return random.choice(weighted_enemies)
        return None

# Location definitions - УЛУЧШЕННЫЕ ЛОКАЦИИ С РЕСУРСАМИ
LOCATIONS = {
    # Central locations
    (2, 2): Location(
        name="Whispering Forest Clearing",
        location_type=LocationType.FOREST,
        description="A peaceful clearing in the heart of the forest. Strange whispers can be heard from the trees. This is a good place to start gathering resources.",
        ascii_art=ASCIIArt.forest,
        connections={'n': (2, 1), 's': (2, 3), 'e': (3, 2), 'w': (1, 2)},
        items=["glowing_moss", "glowing_moss", "healing_shroom", "healing_shroom"],
        is_safe=True
    ),

    # Northern locations
    (2, 1): Location(
        name="Myconid Village",
        location_type=LocationType.VILLAGE,
        description="A village of peaceful mushroom people. They seem friendly but wary of outsiders. This is where you can get quests and information.",
        ascii_art=ASCIIArt.village,
        connections={'s': (2, 2), 'e': (3, 1)},
        npcs=["elder_myconid"],
        is_safe=True
    ),

    (3, 1): Location(
        name="Ancient Laboratory",
        location_type=LocationType.LABORATORY,
        description="An abandoned alchemy laboratory. Broken equipment and strange smells fill the air. You sense powerful knowledge here.",
        ascii_art=None,
        connections={'w': (2, 1)},
        items=["mana_cap", "mana_cap", "vision_fungus", "nightshade", "nightshade"],
        requires_key=True,
        key_item="forest_key",
        is_safe=True  # Safe once unlocked
    ),

    # Southern locations
    (2, 3): Location(
        name="Murky Swamp",
        location_type=LocationType.SWAMP,
        description="A foul-smelling swamp with bubbling pools and strange fungi growing everywhere. The air is thick with spores.",
        ascii_art=ASCIIArt.swamp,
        connections={'n': (2, 2), 'e': (3, 3)},
        enemies=["sporefang", "sporefang", "fungal_ooze", "fungal_ooze"],
        items=["healing_shroom", "nightshade", "nightshade", "glowing_moss"]
    ),

    (3, 3): Location(
        name="Corrupted Grove",
        location_type=LocationType.FOREST,
        description="The trees here are twisted and sickly. A malevolent presence can be felt. This area has been corrupted by dark magic.",
        ascii_art=None,
        connections={'w': (2, 3), 'n': (3, 2)},
        enemies=["thornbeast", "thornbeast", "mindshroom"],
        items=["sun_blossom", "sun_blossom", "nightshade", "vision_fungus"],
        npcs=["corrupted_druid"]
    ),

    # Eastern locations
    (3, 2): Location(
        name="Fungal Caves Entrance",
        location_type=LocationType.CAVE,
        description="The entrance to a network of caves covered in bioluminescent fungi. Strange echoes can be heard from within.",
        ascii_art=ASCIIArt.cave,
        connections={'w': (2, 2), 'e': (4, 2), 's': (3, 3)},
        enemies=["sporefang", "fungal_ooze", "mindshroom"],
        items=["glowing_moss", "glowing_moss", "mana_cap", "healing_shroom"]
    ),

    (4, 2): Location(
        name="Crystal Caverns",
        location_type=LocationType.CAVE,
        description="A beautiful cavern filled with glowing crystals and rare mushrooms. The crystals hum with magical energy.",
        ascii_art=None,
        connections={'w': (3, 2)},
        enemies=["mindshroom", "mindshroom", "thornbeast"],
        items=["mana_cap", "vision_fungus", "vision_fungus", "glowing_moss"],
        requires_key=True,
        key_item="cave_key"
    ),

    # Western locations
    (1, 2): Location(
        name="Mountain Pass",
        location_type=LocationType.MOUNTAIN,
        description="A steep mountain path with treacherous cliffs. Rare plants grow in the cracks. The air is thin and cold.",
        ascii_art=ASCIIArt.mountain,
        connections={'e': (2, 2), 'w': (0, 2)},
        enemies=["thornbeast", "sporefang"],
        items=["sun_blossom", "sun_blossom", "sun_blossom", "nightshade"]
    ),

    (0, 2): Location(
        name="Root Horror's Lair",
        location_type=LocationType.BOSS_ROOM,
        description="A dark cavern where the terrifying Root Horror dwells. The air is thick with spores and the ground trembles with each movement of the beast.",
        ascii_art=None,
        connections={'e': (1, 2)},
        enemies=["root_horror"],
        items=[],  # No regular items in boss room
        is_safe=False
    ),

    # Special locations
    (2, 0): Location(
        name="Balance Altar",
        location_type=LocationType.ALTAR,
        description="An ancient altar dedicated to maintaining balance between plants and fungi. A peaceful energy radiates from this place.",
        ascii_art=None,
        connections={'s': (2, 1)},
        items=["sun_blossom", "healing_shroom", "mana_cap", "glowing_moss"],  # All types of resources
        is_safe=True
    ),

    # Additional forest location
    (1, 1): Location(
        name="Mossy Glade",
        location_type=LocationType.FOREST,
        description="A small glade covered in soft moss. The air is fresh and clean here.",
        ascii_art=ASCIIArt.forest,
        connections={'e': (2, 1), 's': (1, 2)},
        items=["glowing_moss", "glowing_moss", "glowing_moss", "healing_shroom"],
        is_safe=True
    ),

    # Additional cave location
    (4, 1): Location(
        name="Shroom Grotto",
        location_type=LocationType.CAVE,
        description="A small cave filled with various mushrooms. Some glow with soft light.",
        ascii_art=None,
        connections={'w': (3, 1)},
        enemies=["fungal_ooze", "fungal_ooze"],
        items=["healing_shroom", "healing_shroom", "mana_cap", "vision_fungus"]
    )
}

def get_location(x, y):
    """Get location at coordinates"""
    return LOCATIONS.get((x, y))
