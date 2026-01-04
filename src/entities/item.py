"""
Myconaut - Item System
"""

from config import Config
from enum import Enum
from colorama import Style

class ItemType(Enum):
    """Types of items"""
    PLANT = "plant"
    MUSHROOM = "mushroom"
    POTION = "potion"
    KEY = "key"
    EQUIPMENT = "equipment"
    MATERIAL = "material"

class Rarity(Enum):
    """Item rarity"""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"

class Item:
    """Base item class"""

    def __init__(self, id, name, description, item_type, rarity=Rarity.COMMON, value=0, effects=None):
        self.id = id
        self.name = name
        self.description = description
        self.type = item_type
        self.rarity = rarity
        self.value = value
        self.effects = effects or {}
        self.quantity = 1

    def use(self, player):
        """Use the item"""
        if self.type == ItemType.POTION:
            effect = self.effects.get('effect', '')
            magnitude = self.effects.get('magnitude', 0)

            if effect == 'heal':
                player.heal(magnitude)
                Config.print_colored(f"You drink {self.name} and heal {magnitude} HP!", 'success')
            elif effect == 'mana':
                player.restore_mana(magnitude)
                Config.print_colored(f"You drink {self.name} and restore {magnitude} MP!", 'success')
            elif effect == 'hallucination':
                player.add_hallucination(self.effects.get('hallucination_type', 'mild'))
                Config.print_colored(f"You consume {self.name}. The world shifts around you...", 'magic')
            return True

        Config.print_colored(f"Cannot use {self.name} directly.", 'warning')
        return False

    def get_colored_name(self):
        """Get colored name based on rarity"""
        colors = {
            Rarity.COMMON: Config.COLORS['normal'],
            Rarity.UNCOMMON: Config.COLORS['info'],
            Rarity.RARE: Config.COLORS['highlight'],
            Rarity.EPIC: Config.COLORS['magic'],
            Rarity.LEGENDARY: Config.COLORS['title']
        }
        return colors.get(self.rarity, Config.COLORS['normal']) + self.name + Style.RESET_ALL

    def __str__(self):
        return f"{self.get_colored_name()} x{self.quantity}"

class Inventory:
    """Player inventory management"""

    def __init__(self, max_size=20):
        self.max_size = max_size
        self.items = {}
        self.equipped = []

    def add_item(self, item, quantity=1):
        """Add item to inventory"""
        if len(self.items) >= self.max_size and item.id not in self.items:
            Config.print_colored("Inventory is full!", 'error')
            return False

        if item.id in self.items:
            self.items[item.id].quantity += quantity
        else:
            item.quantity = quantity
            self.items[item.id] = item

        Config.print_colored(f"Added {quantity} x {item.name} to inventory.", 'success')
        Config.beep()
        return True

    def remove_item(self, item_id, quantity=1):
        """Remove item from inventory"""
        if item_id in self.items:
            if self.items[item_id].quantity <= quantity:
                del self.items[item_id]
            else:
                self.items[item_id].quantity -= quantity
            return True
        return False

    def has_item(self, item_id, quantity=1):
        """Check if player has item"""
        return item_id in self.items and self.items[item_id].quantity >= quantity

    def display(self):
        """Display inventory"""
        if not self.items:
            Config.print_colored("Your inventory is empty.", 'info')
            return

        Config.print_colored("\n╔══════════════════════════════════════════════════════════════════════╗", 'highlight')
        Config.print_colored("║                            INVENTORY                                 ║", 'highlight')
        Config.print_colored("╠══════════════════════════════════════════════════════════════════════╣", 'highlight')

        for idx, (item_id, item) in enumerate(self.items.items(), 1):
            rarity_color = {
                Rarity.COMMON: '',
                Rarity.UNCOMMON: Config.COLORS['info'],
                Rarity.RARE: Config.COLORS['highlight'],
                Rarity.EPIC: Config.COLORS['magic'],
                Rarity.LEGENDARY: Config.COLORS['title']
            }.get(item.rarity, '')

            print(f"{Config.COLORS['normal']}  [{idx}] {rarity_color}{item.name} x{item.quantity}{Config.COLORS['normal']}")
            print(f"      {item.description}")

        Config.print_colored("╚══════════════════════════════════════════════════════════════════════╝", 'highlight')

    def get_item_by_id(self, item_id):
        """Get item by ID"""
        return self.items.get(item_id)

    def get_items_by_type(self, item_type):
        """Get all items of specific type"""
        return [item for item in self.items.values() if item.type == item_type]

# Predefined items
ITEMS = {
    # Plants
    "glowing_moss": Item(
        id="glowing_moss",
        name="Glowing Moss",
        description="Bioluminescent moss that glows in the dark. Restores 10 MP.",
        item_type=ItemType.PLANT,
        rarity=Rarity.COMMON,
        value=5,
        effects={"effect": "mana", "magnitude": 10}
    ),

    "nightshade": Item(
        id="nightshade",
        name="Nightshade",
        description="A poisonous plant with purple flowers. Can be used in potions.",
        item_type=ItemType.PLANT,
        rarity=Rarity.UNCOMMON,
        value=15,
        effects={"effect": "poison", "magnitude": 5}
    ),

    "sun_blossom": Item(
        id="sun_blossom",
        name="Sun Blossom",
        description="A flower that stores sunlight. Restores 20 HP.",
        item_type=ItemType.PLANT,
        rarity=Rarity.UNCOMMON,
        value=20,
        effects={"effect": "heal", "magnitude": 20}
    ),

    # Mushrooms
    "healing_shroom": Item(
        id="healing_shroom",
        name="Healing Shroom",
        description="A red mushroom with healing properties. Restores 15 HP.",
        item_type=ItemType.MUSHROOM,
        rarity=Rarity.COMMON,
        value=10,
        effects={"effect": "heal", "magnitude": 15}
    ),

    "mana_cap": Item(
        id="mana_cap",
        name="Mana Cap",
        description="A blue mushroom that restores magical energy. Restores 15 MP.",
        item_type=ItemType.MUSHROOM,
        rarity=Rarity.COMMON,
        value=10,
        effects={"effect": "mana", "magnitude": 15}
    ),

    "vision_fungus": Item(
        id="vision_fungus",
        name="Vision Fungus",
        description="A strange mushroom that alters perception. Causes hallucinations.",
        item_type=ItemType.MUSHROOM,
        rarity=Rarity.RARE,
        value=25,
        effects={"effect": "hallucination", "hallucination_type": "vision"}
    ),

    # Potions
    "health_potion": Item(
        id="health_potion",
        name="Health Potion",
        description="A basic healing potion. Restores 30 HP.",
        item_type=ItemType.POTION,
        rarity=Rarity.COMMON,
        value=20,
        effects={"effect": "heal", "magnitude": 30}
    ),

    "mana_elixir": Item(
        id="mana_elixir",
        name="Mana Elixir",
        description="A magical elixir. Restores 40 MP.",
        item_type=ItemType.POTION,
        rarity=Rarity.UNCOMMON,
        value=30,
        effects={"effect": "mana", "magnitude": 40}
    ),

    "balance_tincture": Item(
        id="balance_tincture",
        name="Balance Tincture",
        description="A perfect blend of plant and fungal essences. Restores balance.",
        item_type=ItemType.POTION,
        rarity=Rarity.RARE,
        value=50,
        effects={"effect": "balance", "magnitude": 50}
    ),

    "vision_potion": Item(
        id="vision_potion",
        name="Vision Potion",
        description="A potion that grants psychic visions and reveals hidden truths.",
        item_type=ItemType.POTION,
        rarity=Rarity.RARE,
        value=40,
        effects={"effect": "hallucination", "hallucination_type": "enhanced_vision"}
    ),

    # Keys
    "forest_key": Item(
        id="forest_key",
        name="Forest Key",
        description="An ancient key made of petrified wood.",
        item_type=ItemType.KEY,
        rarity=Rarity.RARE,
        value=50
    ),

    "cave_key": Item(
        id="cave_key",
        name="Crystal Key",
        description="A key made of glowing crystal.",
        item_type=ItemType.KEY,
        rarity=Rarity.RARE,
        value=50
    ),
}

def create_item(item_id):
    """Create an item instance by ID"""
    if item_id in ITEMS:
        item_data = ITEMS[item_id]
        return Item(
            id=item_data.id,
            name=item_data.name,
            description=item_data.description,
            item_type=item_data.type,
            rarity=item_data.rarity,
            value=item_data.value,
            effects=item_data.effects.copy() if item_data.effects else None
        )
    return None
