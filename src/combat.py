"""
Myconaut - Combat System
"""

from config import Config
from src.entities.enemy import create_enemy
from src.ascii_art import ASCIIArt
import random
import time
from src.entities.item import create_item

class Combat:
    """Combat handler"""

    def __init__(self, player, enemy_id):
        self.player = player
        self.enemy = create_enemy(enemy_id)
        self.turn = 0
        self.combat_active = True
        self.escape_attempts = 0
        self.max_escape_attempts = 3
        self.player_effects = {}
        self.enemy_effects = {}

    def start(self):
        """Start combat"""
        Config.clear_screen()
        Config.print_colored(ASCIIArt.create_box("COMBAT ENCOUNTER!"), 'title')

        # Show enemy art based on type
        if hasattr(self.enemy, 'type'):
            if self.enemy.type.value == "sporefang":
                print(ASCIIArt.enemy_sporefang())
            elif self.enemy.type.value == "thornbeast":
                print(ASCIIArt.enemy_thornbeast())
            else:
                Config.print_colored(f"\nA wild {self.enemy.name} appears!\n", 'enemy')
        else:
            Config.print_colored(f"\nA wild {self.enemy.name} appears!\n", 'enemy')

        Config.print_colored(f"You encounter a {self.enemy.name}!", 'enemy')
        Config.beep(2)
        time.sleep(1.5)

        while self.combat_active and self.player.health > 0 and self.enemy.is_alive():
            self.turn += 1
            self.player_turn()

            if self.enemy.is_alive():
                self.enemy_turn()

        self.end_combat()

    def player_turn(self):
        """Player's turn"""
        Config.clear_screen()
        self.display_combat_status()

        print(f"\n{Config.COLORS['highlight']}Turn {self.turn}{Config.COLORS['normal']}")
        Config.print_colored("\nYour turn! Choose an action:", 'info')

        # Display options
        options = [
            ("1", "Attack", "Basic attack with your weapon"),
            ("2", "Ability", "Use a special ability"),
            ("3", "Item", "Use item from inventory"),
            ("4", "Defend", "Raise defense for this turn"),
            ("5", "Escape", "Try to escape from combat")
        ]

        for key, action, desc in options:
            Config.print_colored(f"  [{key}] {action:12} - {desc}", 'normal')

        choice = input("\nChoose action: ").strip()

        if choice == "1":
            self.player_attack()
        elif choice == "2":
            self.use_ability()
        elif choice == "3":
            self.use_item()
        elif choice == "4":
            self.player_defend()
        elif choice == "5":
            self.attempt_escape()
        else:
            Config.print_colored("Invalid choice! You hesitate and lose time.", 'warning')

    def player_attack(self):
        """Player basic attack"""
        # Check for stun effects
        if self.player_effects.get("stunned", 0) > 0:
            Config.print_colored("You are stunned and cannot attack!", 'error')
            self.player_effects["stunned"] -= 1
            return

        # Calculate base damage
        base_damage = self.player.base_damage

        # Apply any attack buffs
        if self.player_effects.get("attack_buff", 0) > 0:
            base_damage = int(base_damage * 1.5)
            self.player_effects["attack_buff"] -= 1

        # Critical hit chance
        damage = base_damage
        crit_roll = random.random()

        if crit_roll < self.player.crit_chance:
            damage *= 2
            Config.print_colored("CRITICAL HIT!", 'title')
            Config.beep()

        # Enemy defense
        actual_damage = max(1, damage - self.enemy_effects.get("defense", 0))

        # Apply damage
        actual_damage = self.enemy.take_damage(actual_damage)

        Config.print_colored(f"\nYou attack the {self.enemy.name} for {actual_damage} damage!", 'success')

        if not self.enemy.is_alive():
            Config.print_colored(f"The {self.enemy.name} is defeated!", 'title')
            Config.beep(3)

    def player_defend(self):
        """Player defends, increasing defense"""
        self.player_effects["defense"] = self.player_effects.get("defense", 0) + 5
        Config.print_colored("\nYou take a defensive stance. Your defense increases!", 'success')

    def use_ability(self):
        """Use player ability"""
        if self.player_effects.get("stunned", 0) > 0:
            Config.print_colored("You are stunned and cannot use abilities!", 'error')
            self.player_effects["stunned"] -= 1
            return

        if not hasattr(self.player, 'abilities') or not self.player.abilities:
            Config.print_colored("You don't have any abilities!", 'warning')
            return

        Config.print_colored("\nAvailable abilities:", 'highlight')

        # Get actual abilities from player
        abilities = self.get_player_abilities()

        if not abilities:
            Config.print_colored("You don't have any abilities available!", 'warning')
            return

        for i, (ability_name, mana_cost, effect) in enumerate(abilities, 1):
            Config.print_colored(f"  [{i}] {ability_name} ({mana_cost} MP)", 'info')

        try:
            choice = int(input("\nChoose ability (0 to cancel): ")) - 1
            if choice == -1:
                return

            if 0 <= choice < len(abilities):
                ability_name, mana_cost, effect = abilities[choice]

                if self.player.mana < mana_cost:
                    Config.print_colored("Not enough mana!", 'error')
                    return

                self.player.mana -= mana_cost
                self.use_player_ability(ability_name, effect)
            else:
                Config.print_colored("Invalid ability choice!", 'error')
        except ValueError:
            Config.print_colored("Invalid input!", 'error')

    def get_player_abilities(self):
        """Get player abilities based on level"""
        abilities = []

        # All players start with basic abilities
        abilities.append(("Fungal Spore Burst", 10, "damage"))

        if self.player.level >= 2:
            abilities.append(("Photosynthesis", 15, "heal"))

        if self.player.level >= 3:
            abilities.append(("Mycelium Network", 5, "reveal"))

        if self.player.level >= 4:
            abilities.append(("Poison Dart", 12, "poison"))

        if self.player.level >= 5:
            abilities.append(("Balance Trance", 20, "buff"))

        return abilities

    def use_player_ability(self, ability_name, effect):
        """Use a specific player ability"""
        if effect == "damage":
            damage = self.player.base_damage * 1.5
            actual_damage = self.enemy.take_damage(damage)
            Config.print_colored(f"\nYou unleash {ability_name} for {actual_damage} damage!", 'success')

        elif effect == "heal":
            heal_amount = self.player.max_health // 3
            self.player.heal(heal_amount)
            Config.print_colored(f"\nYou use {ability_name} and heal {heal_amount} HP!", 'success')

        elif effect == "reveal":
            Config.print_colored(f"\nYou use {ability_name} and sense the enemy's weaknesses!", 'info')
            self.enemy_effects["vulnerable"] = 3  # Takes more damage for 3 turns

        elif effect == "poison":
            self.enemy_effects["poisoned"] = 3  # Poison for 3 turns
            Config.print_colored(f"\nYou poison the {self.enemy.name} with {ability_name}!", 'success')

        elif effect == "buff":
            self.player_effects["attack_buff"] = 3
            self.player_effects["defense"] = self.player_effects.get("defense", 0) + 3
            Config.print_colored(f"\nYou enter {ability_name}. Attack and defense increased!", 'success')

    def use_item(self):
        """Use item from inventory"""
        if self.player_effects.get("stunned", 0) > 0:
            Config.print_colored("You are stunned and cannot use items!", 'error')
            self.player_effects["stunned"] -= 1
            return

        if not hasattr(self.player, 'inventory') or not self.player.inventory.items:
            Config.print_colored("Your inventory is empty!", 'warning')
            return

        self.player.inventory.display()

        try:
            choice = int(input("\nChoose item to use (0 to cancel): "))
            if choice == 0:
                return

            items_list = list(self.player.inventory.items.values())
            if 1 <= choice <= len(items_list):
                item = items_list[choice - 1]

                # Check if item can be used in combat
                if hasattr(item, 'use'):
                    if item.use(self.player):
                        self.player.inventory.remove_item(item.id, 1)
                        Config.print_colored(f"You use {item.name}!", 'success')
                    else:
                        Config.print_colored(f"Cannot use {item.name} in combat!", 'warning')
                else:
                    Config.print_colored(f"Cannot use {item.name} directly.", 'warning')
            else:
                Config.print_colored("Invalid item choice!", 'error')
        except ValueError:
            Config.print_colored("Invalid input!", 'error')

    def attempt_escape(self):
        """Try to escape from combat"""
        self.escape_attempts += 1

        if self.escape_attempts >= self.max_escape_attempts:
            Config.print_colored("The enemy blocks your escape route!", 'error')
            return

        # Base escape chance
        escape_chance = 0.4

        # Bonuses
        if self.player.dodge_chance > 0.2:
            escape_chance += 0.2

        if self.player.level > self.enemy.xp_reward // 25:  # Rough level comparison
            escape_chance += 0.1

        if random.random() < escape_chance:
            Config.print_colored("You successfully escape from combat!", 'success')
            self.combat_active = False
            # Lose some HP when escaping
            escape_damage = self.player.max_health // 10
            self.player.take_damage(escape_damage)
            Config.print_colored(f"You take {escape_damage} damage while escaping!", 'warning')
        else:
            Config.print_colored("Escape failed! The enemy presses the attack!", 'error')
            Config.beep()

    def enemy_turn(self):
        """Enemy's turn"""
        if not self.enemy.is_alive():
            return

        Config.print_colored(f"\n{self.enemy.name}'s turn!", 'enemy')
        time.sleep(1.5)

        # Apply poison damage if enemy is poisoned
        if self.enemy_effects.get("poisoned", 0) > 0:
            poison_damage = self.enemy.max_health // 20
            self.enemy.take_damage(poison_damage)
            Config.print_colored(f"The {self.enemy.name} takes {poison_damage} poison damage!", 'success')
            self.enemy_effects["poisoned"] -= 1

        # Check if enemy can act
        if self.enemy_effects.get("stunned", 0) > 0:
            Config.print_colored(f"The {self.enemy.name} is stunned and cannot act!", 'success')
            self.enemy_effects["stunned"] -= 1
            return

        # Chance to use special attack
        use_special = False
        if hasattr(self.enemy, 'special_ability') and self.enemy.special_ability:
            # Higher chance to use special when enemy is low on health
            health_percent = self.enemy.health / self.enemy.max_health
            if health_percent < 0.3:
                use_special = random.random() < 0.6  # 60% chance when low health
            else:
                use_special = random.random() < 0.3  # 30% chance normally

        if use_special:
            self.enemy.special_attack(self.player)
        else:
            # Regular attack
            if self.player.can_dodge():
                Config.print_colored(f"You dodge the {self.enemy.name}'s attack!", 'success')
            else:
                # Calculate enemy damage
                damage = self.enemy.attack()

                # Apply player defense
                if self.player_effects.get("defense", 0) > 0:
                    damage = max(1, damage - self.player_effects["defense"])
                    self.player_effects["defense"] = max(0, self.player_effects["defense"] - 2)

                actual_damage = self.player.take_damage(damage)
                Config.print_colored(f"The {self.enemy.name} attacks you for {actual_damage} damage!", 'error')

                # Chance for enemy to apply debuff
                if random.random() < 0.1:  # 10% chance
                    self.player_effects["stunned"] = 1
                    Config.print_colored(f"The {self.enemy.name} stuns you!", 'error')

        if self.player.health <= 0:
            Config.print_colored("You have been defeated!", 'error')

        time.sleep(2)

    def display_combat_status(self):
        """Display combat status"""
        Config.print_colored("\n╔══════════════════════════════════════════════════════════════════════╗", 'highlight')
        Config.print_colored("║                            COMBAT STATUS                            ║", 'highlight')
        Config.print_colored("╠══════════════════════════════════════════════════════════════════════╣", 'highlight')

        # Player stats
        Config.print_colored(f"\n{self.player.name}", 'title')
        health_percent = (self.player.health / self.player.max_health) * 100
        health_bar = "█" * int(health_percent / 5) + "░" * (20 - int(health_percent / 5))
        Config.print_colored(f"HP: {self.player.health}/{self.player.max_health} [{health_bar}]", 'health')

        mana_percent = (self.player.mana / self.player.max_mana) * 100
        mana_bar = "█" * int(mana_percent / 5) + "░" * (20 - int(mana_percent / 5))
        Config.print_colored(f"MP: {self.player.mana}/{self.player.max_mana} [{mana_bar}]\n", 'mana')

        # Player effects
        if self.player_effects:
            Config.print_colored("Player Effects:", 'info')
            for effect, duration in self.player_effects.items():
                if duration > 0:
                    Config.print_colored(f"  • {effect.replace('_', ' ').title()}: {duration} turns", 'info')

        # Enemy stats
        Config.print_colored(f"\n{self.enemy.name}", 'enemy')
        enemy_health_percent = (self.enemy.health / self.enemy.max_health) * 100
        enemy_health_bar = "█" * int(enemy_health_percent / 5) + "░" * (20 - int(enemy_health_percent / 5))
        Config.print_colored(f"HP: {self.enemy.health}/{self.enemy.max_health} [{enemy_health_bar}]", 'health')

        # Enemy effects
        if self.enemy_effects:
            Config.print_colored("Enemy Effects:", 'info')
            for effect, duration in self.enemy_effects.items():
                if duration > 0:
                    Config.print_colored(f"  • {effect.replace('_', ' ').title()}: {duration} turns", 'info')

        Config.print_colored("\n╚══════════════════════════════════════════════════════════════════════╝", 'highlight')

    def end_combat(self):
        """End combat and handle rewards"""
        if not self.enemy.is_alive():
            # Player wins
            Config.print_colored(f"\n╔══════════════════════════════════════════════════════════════════════╗", 'title')
            Config.print_colored(f"║                          VICTORY!                                    ║", 'title')
            Config.print_colored(f"╚══════════════════════════════════════════════════════════════════════╝", 'title')

            Config.print_colored(f"You defeated the {self.enemy.name}!", 'title')
            Config.beep(3)
            time.sleep(1)

            # XP reward
            xp_reward = self.enemy.xp_reward
            self.player.add_xp(xp_reward)

            # Loot drops
            loot = self.enemy.get_loot()
            if loot:
                Config.print_colored("\nThe enemy dropped:", 'item')
                for item_id in loot:
                    item = create_item(item_id)
                    if item:
                        self.player.inventory.add_item(item)

            # Chance for hallucination from certain enemies
            if hasattr(self.enemy, 'type') and self.enemy.type.value == "mindshroom":
                if random.random() < 0.5:
                    self.player.add_hallucination("psychic_echo")
                    Config.print_colored("\nThe mindshroom's psychic energy lingers in your mind...", 'magic')

            # Chance for extra reward on critical kills
            if random.random() < 0.1:  # 10% chance
                bonus_items = ["mana_cap", "healing_shroom", "glowing_moss"]
                bonus_item = random.choice(bonus_items)
                item = create_item(bonus_item)
                if item:
                    self.player.inventory.add_item(item)
                    Config.print_colored(f"You find an extra {item.name} on the enemy's remains!", 'item')

            time.sleep(2)

        elif self.player.health <= 0:
            # Player loses
            Config.print_colored("\nYou have been defeated...", 'error')
            Config.beep()
            time.sleep(2)

        # Reset effects
        self.player_effects = {}
        self.enemy_effects = {}
        self.escape_attempts = 0
