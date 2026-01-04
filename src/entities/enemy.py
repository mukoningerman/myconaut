"""
Myconaut - Enemy System
"""

from config import Config
import random
from enum import Enum

class EnemyType(Enum):
    """Types of enemies"""
    SPOREFANG = "sporefang"
    THORNBEAST = "thornbeast"
    MINDSHROOM = "mindshroom"
    ROOT_HORROR = "root_horror"
    FUNGAL_OOZE = "fungal_ooze"

class Enemy:
    """Base enemy class"""

    def __init__(self, name, enemy_type, health, damage, xp_reward, loot=None):
        self.name = name
        self.type = enemy_type
        self.max_health = health
        self.health = health
        self.damage = damage
        self.xp_reward = xp_reward
        self.loot = loot or []
        self.special_ability = None

    def take_damage(self, amount):
        """Take damage"""
        self.health = max(0, self.health - amount)
        return amount

    def is_alive(self):
        """Check if enemy is alive"""
        return self.health > 0

    def attack(self):
        """Perform an attack"""
        return self.damage

    def special_attack(self, player):
        """Perform special attack if available"""
        if self.special_ability:
            return self.special_ability.execute(self, player)
        return None

    def get_loot(self):
        """Generate loot drops"""
        dropped_loot = []
        for item_id, chance in self.loot:
            if random.random() < chance:
                dropped_loot.append(item_id)
        return dropped_loot

    def display_health(self):
        """Display health bar"""
        health_percent = (self.health / self.max_health) * 100
        health_bar = "█" * int(health_percent / 5) + "░" * (20 - int(health_percent / 5))
        Config.print_colored(f"\n{self.name}", 'enemy')
        Config.print_colored(f"HP: {self.health}/{self.max_health} [{health_bar}]", 'health')

# Enemy definitions
ENEMIES = {
    "sporefang": Enemy(
        name="Sporefang",
        enemy_type=EnemyType.SPOREFANG,
        health=30,
        damage=8,
        xp_reward=25,
        loot=[("healing_shroom", 0.5), ("glowing_moss", 0.3)]
    ),

    "thornbeast": Enemy(
        name="Thornbeast",
        enemy_type=EnemyType.THORNBEAST,
        health=50,
        damage=12,
        xp_reward=40,
        loot=[("nightshade", 0.4), ("sun_blossom", 0.2)]
    ),

    "mindshroom": Enemy(
        name="Mindshroom",
        enemy_type=EnemyType.MINDSHROOM,
        health=40,
        damage=6,
        xp_reward=35,
        loot=[("vision_fungus", 0.6), ("mana_cap", 0.4)]
    ),

    "fungal_ooze": Enemy(
        name="Fungal Ooze",
        enemy_type=EnemyType.FUNGAL_OOZE,
        health=25,
        damage=5,
        xp_reward=20,
        loot=[("healing_shroom", 0.7), ("glowing_moss", 0.5)]
    ),

    "root_horror": Enemy(
        name="Root Horror",
        enemy_type=EnemyType.ROOT_HORROR,
        health=100,
        damage=20,
        xp_reward=100,
        loot=[("forest_key", 1.0), ("sun_blossom", 0.8)]
    )
}

class SpecialAbility:
    """Base class for enemy special abilities"""

    def __init__(self, name, description, effect):
        self.name = name
        self.description = description
        self.effect = effect

    def execute(self, enemy, player):
        """Execute the ability"""
        if self.effect == "poison":
            poison_damage = enemy.damage // 2
            player.take_damage(poison_damage)
            Config.print_colored(f"{enemy.name} poisons you for {poison_damage} damage!", 'error')
            return poison_damage
        elif self.effect == "mana_drain":
            drain_amount = 15
            player.mana = max(0, player.mana - drain_amount)
            Config.print_colored(f"{enemy.name} drains {drain_amount} MP from you!", 'error')
            return 0
        elif self.effect == "hallucinate":
            player.add_hallucination("enemy_visions")
            Config.print_colored(f"{enemy.name} causes you to hallucinate!", 'magic')
            return 0

        return 0

# Assign special abilities
ENEMIES["mindshroom"].special_ability = SpecialAbility(
    "Psychic Blast",
    "Drains mana and causes confusion",
    "mana_drain"
)

ENEMIES["thornbeast"].special_ability = SpecialAbility(
    "Toxic Thorns",
    "Poisons the target",
    "poison"
)

def create_enemy(enemy_id):
    """Create an enemy instance by ID"""
    if enemy_id in ENEMIES:
        enemy_data = ENEMIES[enemy_id]
        enemy = Enemy(
            name=enemy_data.name,
            enemy_type=enemy_data.type,
            health=enemy_data.max_health,
            damage=enemy_data.damage,
            xp_reward=enemy_data.xp_reward,
            loot=enemy_data.loot.copy() if enemy_data.loot else []
        )

        if enemy_data.special_ability:
            enemy.special_ability = enemy_data.special_ability

        return enemy

    return None
