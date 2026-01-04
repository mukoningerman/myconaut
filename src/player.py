"""
Myconaut - Player Class
"""

from ascii_art import ASCIIArt
from config import Config
from src.entities.item import Inventory, ItemType, Rarity
import random

class Player:
    def __init__(self, name):
        self.name = name
        self.level = Config.STARTING_LEVEL
        self.xp = 0
        self.xp_to_next = Config.LEVEL_UP_XP

        # Stats
        self.max_health = Config.STARTING_HEALTH
        self.health = Config.STARTING_HEALTH
        self.max_mana = Config.STARTING_MANA
        self.mana = Config.STARTING_MANA

        # Combat stats
        self.base_damage = Config.BASE_DAMAGE
        self.defense = 5
        self.crit_chance = Config.CRIT_CHANCE
        self.dodge_chance = Config.DODGE_CHANCE

        # Progression
        self.skill_points = 0
        self.abilities_learned = []  # List of ability IDs
        self.discovered_recipes = []

        # State
        self.inventory = Inventory()
        self.current_location = (2, 2)  # Center of map
        self.visited_locations = set()
        self.active_effects = {}
        self.hallucinations = []
        self.completed_quests = []
        self.active_quests = []

        # Story flags
        self.story_progress = 0
        self.has_met_elder = False
        self.has_met_druid = False
        self.found_laboratory = False
        self.defeated_root_horror = False

        # Statistics
        self.enemies_defeated = 0
        self.items_collected = 0
        self.potions_brewed = 0
        self.times_died = 0

    def heal(self, amount):
        """Heal the player"""
        old_health = self.health
        self.health = min(self.max_health, self.health + amount)
        actual_heal = self.health - old_health
        if actual_heal > 0:
            Config.print_colored(f"Health restored by {actual_heal}!", 'success')
        return actual_heal

    def restore_mana(self, amount):
        """Restore mana"""
        old_mana = self.mana
        self.mana = min(self.max_mana, self.mana + amount)
        actual_restore = self.mana - old_mana
        if actual_restore > 0:
            Config.print_colored(f"Mana restored by {actual_restore}!", 'success')
        return actual_restore

    def take_damage(self, amount):
        """Take damage with defense calculation"""
        # Calculate damage reduction from defense
        defense_reduction = self.defense * 0.5  # Each defense point reduces damage by 0.5
        actual_damage = max(1, int(amount - defense_reduction))

        # Critical damage chance (enemy crit)
        if random.random() < 0.05:  # 5% chance for enemy critical
            actual_damage *= 2
            Config.print_colored("ENEMY CRITICAL HIT!", 'error')

        old_health = self.health
        self.health = max(0, self.health - actual_damage)

        # Check if player died
        if self.health <= 0:
            self.times_died += 1

        return actual_damage

    def add_xp(self, amount):
        """Add experience points"""
        self.xp += amount
        Config.print_colored(f"Gained {amount} XP!", 'xp')

        # Check for level up
        while self.xp >= self.xp_to_next:
            self.level_up()

    def level_up(self):
        """Level up the player"""
        self.level += 1
        self.xp -= self.xp_to_next
        self.xp_to_next = int(self.xp_to_next * Config.XP_MULTIPLIER)

        # Stat increases
        health_increase = 20 + (self.level * 2)
        mana_increase = 10 + self.level

        self.max_health += health_increase
        self.health = self.max_health
        self.max_mana += mana_increase
        self.mana = self.max_mana
        self.base_damage += 3 + (self.level // 3)
        self.defense += 2

        # Every 3 levels, increase crit and dodge chance slightly
        if self.level % 3 == 0:
            self.crit_chance += 0.02
            self.dodge_chance += 0.015

        self.skill_points += 1

        # Learn new abilities at certain levels
        if self.level == 2 and "photosynthesis" not in self.abilities_learned:
            self.abilities_learned.append("photosynthesis")
        elif self.level == 3 and "mycelium_network" not in self.abilities_learned:
            self.abilities_learned.append("mycelium_network")
        elif self.level == 4 and "poison_dart" not in self.abilities_learned:
            self.abilities_learned.append("poison_dart")
        elif self.level == 5 and "balance_trance" not in self.abilities_learned:
            self.abilities_learned.append("balance_trance")

        Config.clear_screen()
        Config.print_colored("╔══════════════════════════════════════════════════════════════════════╗", 'title')
        Config.print_colored("║                             LEVEL UP!                               ║", 'title')
        Config.print_colored("╚══════════════════════════════════════════════════════════════════════╝", 'title')

        Config.print_colored(f"\nCongratulations! You are now level {self.level}!", 'highlight')
        Config.print_colored(f"\nStat increases:", 'info')
        Config.print_colored(f"  Health: +{health_increase} (now {self.max_health})", 'health')
        Config.print_colored(f"  Mana: +{mana_increase} (now {self.max_mana})", 'mana')
        Config.print_colored(f"  Damage: +{3 + (self.level // 3)} (now {self.base_damage})", 'highlight')
        Config.print_colored(f"  Defense: +2 (now {self.defense})", 'info')

        if self.level % 3 == 0:
            Config.print_colored(f"  Crit Chance: +2% (now {self.crit_chance*100:.1f}%)", 'highlight')
            Config.print_colored(f"  Dodge Chance: +1.5% (now {self.dodge_chance*100:.1f}%)", 'info')

        if self.level in [2, 3, 4, 5]:
            new_ability = {
                2: "Photosynthesis (heal)",
                3: "Mycelium Network (reveal secrets)",
                4: "Poison Dart (poison enemy)",
                5: "Balance Trance (buff)"
            }[self.level]
            Config.print_colored(f"\nNew ability learned: {new_ability}!", 'quest')

        Config.print_colored(f"\nSkill points available: {self.skill_points}", 'quest')
        Config.print_colored("You can spend skill points to improve your stats.", 'info')

        Config.beep(3)
        input("\nPress Enter to continue...")

    def spend_skill_point(self, stat):
        """Spend a skill point to improve a stat"""
        if self.skill_points <= 0:
            Config.print_colored("You don't have any skill points!", 'error')
            return False

        improvements = {
            "health": lambda: setattr(self, 'max_health', self.max_health + 30),
            "mana": lambda: setattr(self, 'max_mana', self.max_mana + 20),
            "damage": lambda: setattr(self, 'base_damage', self.base_damage + 5),
            "defense": lambda: setattr(self, 'defense', self.defense + 3),
            "crit": lambda: setattr(self, 'crit_chance', self.crit_chance + 0.03),
            "dodge": lambda: setattr(self, 'dodge_chance', self.dodge_chance + 0.02)
        }

        if stat in improvements:
            improvements[stat]()
            self.skill_points -= 1

            # Also heal/restore when increasing max stats
            if stat == "health":
                self.health = self.max_health
            elif stat == "mana":
                self.mana = self.max_mana

            Config.print_colored(f"You improved your {stat}!", 'success')
            return True

        Config.print_colored("Invalid stat to improve!", 'error')
        return False

    def get_abilities(self):
        """Get list of available abilities"""
        abilities = []

        # Basic ability everyone has
        abilities.append(("Fungal Spore Burst", 10, "damage", "Launch a burst of toxic spores at the enemy"))

        # Learned abilities
        if "photosynthesis" in self.abilities_learned:
            abilities.append(("Photosynthesis", 15, "heal", "Absorb sunlight to heal yourself"))

        if "mycelium_network" in self.abilities_learned:
            abilities.append(("Mycelium Network", 5, "reveal", "Connect to the fungal network to reveal enemy weaknesses"))

        if "poison_dart" in self.abilities_learned:
            abilities.append(("Poison Dart", 12, "poison", "Shoot a poisonous dart that damages over time"))

        if "balance_trance" in self.abilities_learned:
            abilities.append(("Balance Trance", 20, "buff", "Enter a trance that increases all stats temporarily"))

        return abilities

    def add_hallucination(self, hallucination_type):
        """Add a hallucination effect"""
        if hallucination_type not in self.hallucinations:
            self.hallucinations.append(hallucination_type)
            Config.print_colored("Reality shifts around you...", 'magic')

    def remove_hallucination(self, hallucination_type):
        """Remove a hallucination effect"""
        if hallucination_type in self.hallucinations:
            self.hallucinations.remove(hallucination_type)

    def add_recipe(self, recipe_id):
        """Add a discovered recipe"""
        if recipe_id not in self.discovered_recipes:
            self.discovered_recipes.append(recipe_id)
            Config.print_colored("You discovered a new alchemy recipe!", 'success')

    def has_recipe(self, recipe_id):
        """Check if player knows a recipe"""
        return recipe_id in self.discovered_recipes

    def get_attack_damage(self):
        """Calculate attack damage"""
        damage = self.base_damage

        # Apply any active buffs
        if self.active_effects.get("attack_buff", 0) > 0:
            damage = int(damage * 1.5)

        # Critical hit chance
        if random.random() < self.crit_chance:
            damage *= 2
            return damage, True  # Return damage and crit flag

        return damage, False

    def can_dodge(self):
        """Check if player dodges"""
        dodge_chance = self.dodge_chance

        # Apply any dodge buffs
        if self.active_effects.get("dodge_buff", 0) > 0:
            dodge_chance += 0.2

        return random.random() < dodge_chance

    def use_ability(self, ability_name, target):
        """Use an ability on target"""
        abilities = self.get_abilities()

        for name, mana_cost, effect, description in abilities:
            if name == ability_name:
                if self.mana < mana_cost:
                    return False, "Not enough mana"

                self.mana -= mana_cost

                # Track ability usage
                self.items_collected += 1  # Using this to track ability uses

                return True, effect

        return False, "Ability not found"

    def display_stats(self):
        """Display player stats"""
        health_percent = (self.health / self.max_health) * 100
        mana_percent = (self.mana / self.max_mana) * 100

        health_bar = "█" * int(health_percent / 5) + "░" * (20 - int(health_percent / 5))
        mana_bar = "█" * int(mana_percent / 5) + "░" * (20 - int(mana_percent / 5))

        Config.print_colored("\n" + ASCIIArt.player(), 'highlight')
        Config.print_colored(f"\n{self.name} - Level {self.level}", 'title')
        Config.print_colored(f"XP: {self.xp}/{self.xp_to_next} ({self.xp_to_next - self.xp} to next level)", 'xp')

        Config.print_colored(f"\nHealth: {self.health}/{self.max_health}", 'health')
        Config.print_colored(f"[{health_bar}]", 'health')

        Config.print_colored(f"\nMana: {self.mana}/{self.max_mana}", 'mana')
        Config.print_colored(f"[{mana_bar}]", 'mana')

        Config.print_colored(f"\nDamage: {self.base_damage}", 'normal')
        Config.print_colored(f"Defense: {self.defense}", 'normal')
        Config.print_colored(f"Crit Chance: {self.crit_chance*100:.1f}%", 'normal')
        Config.print_colored(f"Dodge Chance: {self.dodge_chance*100:.1f}%", 'normal')

        # Active effects
        if self.active_effects:
            Config.print_colored(f"\nActive Effects:", 'magic')
            for effect, duration in self.active_effects.items():
                if duration > 0:
                    Config.print_colored(f"  • {effect.replace('_', ' ').title()}: {duration} turns", 'magic')

        # Abilities
        abilities = self.get_abilities()
        if abilities:
            Config.print_colored("\nAbilities:", 'highlight')
            for i, (name, mana_cost, effect, description) in enumerate(abilities, 1):
                Config.print_colored(f"  {i}. {name} ({mana_cost} MP)", 'info')
                Config.print_colored(f"     {description}", 'normal')

        # Hallucinations
        if self.hallucinations:
            Config.print_colored("\nActive Hallucinations:", 'magic')
            for h in self.hallucinations:
                Config.print_colored(f"  • {h.replace('_', ' ').title()}", 'magic')

        # Skill points
        if self.skill_points > 0:
            Config.print_colored(f"\nSkill points available: {self.skill_points}", 'quest')
            Config.print_colored("Use 'C' then choose 'Improve Stats' to spend them.", 'info')

        # Statistics
        Config.print_colored("\nStatistics:", 'info')
        Config.print_colored(f"  Enemies defeated: {self.enemies_defeated}", 'normal')
        Config.print_colored(f"  Items collected: {self.items_collected}", 'normal')
        Config.print_colored(f"  Potions brewed: {self.potions_brewed}", 'normal')
        Config.print_colored(f"  Locations discovered: {len(self.visited_locations)}", 'normal')
        Config.print_colored(f"  Quests completed: {len(self.completed_quests)}", 'normal')

    def save_data(self):
        """Prepare player data for saving - ensure all data is JSON serializable"""
        return {
            'name': self.name,
            'level': self.level,
            'xp': self.xp,
            'xp_to_next': self.xp_to_next,
            'health': self.health,
            'max_health': self.max_health,
            'mana': self.mana,
            'max_mana': self.max_mana,
            'base_damage': self.base_damage,
            'defense': self.defense,
            'crit_chance': self.crit_chance,
            'dodge_chance': self.dodge_chance,
            'skill_points': self.skill_points,
            'abilities_learned': self.abilities_learned,
            'current_location': list(self.current_location),  # Сохраняем как список
            'visited_locations': [list(loc) for loc in self.visited_locations],  # Все как списки
            'hallucinations': self.hallucinations,
            'discovered_recipes': self.discovered_recipes,
            'completed_quests': self.completed_quests,
            'active_quests': self.active_quests,
            'story_progress': self.story_progress,
            'has_met_elder': self.has_met_elder,
            'has_met_druid': self.has_met_druid,
            'found_laboratory': self.found_laboratory,
            'defeated_root_horror': self.defeated_root_horror,
            'enemies_defeated': self.enemies_defeated,
            'items_collected': self.items_collected,
            'potions_brewed': self.potions_brewed,
            'times_died': self.times_died
        }

    def load_data(self, data):
        """Load player data from save"""
        self.name = data['name']
        self.level = data['level']
        self.xp = data['xp']
        self.xp_to_next = data['xp_to_next']
        self.health = data['health']
        self.max_health = data['max_health']
        self.mana = data['mana']
        self.max_mana = data['max_mana']
        self.base_damage = data['base_damage']
        self.defense = data['defense']
        self.crit_chance = data['crit_chance']
        self.dodge_chance = data['dodge_chance']
        self.skill_points = data['skill_points']
        self.abilities_learned = data['abilities_learned']

        # Обработка current_location - преобразуем в кортеж
        current_loc = data['current_location']
        if isinstance(current_loc, list):
            self.current_location = tuple(current_loc)
        else:
            self.current_location = current_loc

        # Обработка visited_locations - преобразуем списки в кортежи
        visited_data = data['visited_locations']
        self.visited_locations = set()
        for loc in visited_data:
            if isinstance(loc, list):
                self.visited_locations.add(tuple(loc))
            elif isinstance(loc, tuple):
                self.visited_locations.add(loc)
            else:
                # Попытка преобразовать строку или другие типы
                try:
                    self.visited_locations.add(tuple(loc))
                except:
                    # Если не получается, просто добавляем как есть
                    self.visited_locations.add(loc)

        self.hallucinations = data['hallucinations']
        self.discovered_recipes = data['discovered_recipes']
        self.completed_quests = data['completed_quests']
        self.active_quests = data['active_quests']
        self.story_progress = data['story_progress']
        self.has_met_elder = data['has_met_elder']
        self.has_met_druid = data['has_met_druid']
        self.found_laboratory = data['found_laboratory']
        self.defeated_root_horror = data['defeated_root_horror']
        self.enemies_defeated = data['enemies_defeated']
        self.items_collected = data['items_collected']
        self.potions_brewed = data['potions_brewed']
        self.times_died = data['times_died']
