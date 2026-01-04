"""
Myconaut - NPC and Dialogue System
"""

from config import Config
from src.ascii_art import ASCIIArt
from src.entities.item import create_item
import random
import time

class NPC:
    """Non-Player Character"""

    def __init__(self, id, name, description, dialogue_tree, art_function=None):
        self.id = id
        self.name = name
        self.description = description
        self.dialogue_tree = dialogue_tree
        self.art_function = art_function
        self.met = False
        self.dialogue_state = "initial"

    def display(self):
        """Display NPC"""
        if self.art_function:
            print(self.art_function())
        else:
            Config.print_colored(f"\n[{self.name}]", 'npc')

    def talk(self, player):
        """Start dialogue with NPC"""
        self.display()

        if not self.met:
            Config.print_colored(f"You meet {self.name}. {self.description}", 'npc')
            self.met = True
            Config.beep()
            time.sleep(1)
        else:
            Config.print_colored(f"{self.name} greets you.", 'npc')

        # Main dialogue loop
        while True:
            # Update dialogue state based on player progress
            self.update_dialogue_state(player)

            # Get current dialogue
            dialogue = self.dialogue_tree.get(self.dialogue_state, {})
            text = dialogue.get('text', f"{self.name} has nothing to say.")
            options = dialogue.get('options', [])

            # Display dialogue
            Config.clear_screen()
            self.display()
            Config.print_colored(f"\n{self.name}: {text}\n", 'npc')

            if not options:
                input("\nPress Enter to continue...")
                return None

            # Display options
            for i, (option_text, result) in enumerate(options, 1):
                Config.print_colored(f"  [{i}] {option_text}", 'info')

            Config.print_colored(f"  [0] End conversation with {self.name}", 'warning')

            # Get player choice
            try:
                choice = int(input("\nYour response: ")) - 1

                if choice == -1:  # Player chose to leave
                    Config.print_colored(f"\nYou end the conversation with {self.name}.", 'info')
                    time.sleep(1)
                    return None

                if 0 <= choice < len(options):
                    option_text, result = options[choice]

                    # Show what player said
                    Config.print_colored(f"\nYou: {option_text}", 'highlight')
                    time.sleep(0.5)

                    # Handle the result
                    if isinstance(result, str):
                        if result.startswith("state:"):
                            new_state = result.split(":")[1]
                            self.dialogue_state = new_state
                        elif result == "quest:start":
                            return "start_quest"
                        elif result == "quest:complete":
                            return "complete_quest"
                        elif result == "trade":
                            return "trade"
                        elif result == "leave":
                            Config.print_colored(f"\n{self.name}: Farewell, traveler.", 'npc')
                            time.sleep(1)
                            return None
                        else:
                            # Just text response
                            Config.print_colored(f"\n{self.name}: {result}", 'npc')
                            input("\nPress Enter to continue...")

                    elif isinstance(result, dict):
                        # Complex result with effects
                        if 'text' in result:
                            Config.print_colored(f"\n{self.name}: {result['text']}", 'npc')

                        if 'xp' in result:
                            player.add_xp(result['xp'])
                            Config.print_colored(f"\nYou gain {result['xp']} experience!", 'xp')

                        if 'item' in result:
                            item = create_item(result['item'])
                            if item:
                                player.inventory.add_item(item)
                                Config.print_colored(f"\n{self.name} gives you: {item.name}", 'item')

                        if 'recipe' in result:
                            player.add_recipe(result['recipe'])
                            Config.print_colored(f"\nYou learn the {result['recipe'].replace('_', ' ').title()} recipe!", 'success')

                        if 'next_state' in result:
                            self.dialogue_state = result['next_state']

                        if 'trigger' in result:
                            if result['trigger'] == "met_elder":
                                player.has_met_elder = True
                            elif result['trigger'] == "met_druid":
                                player.has_met_druid = True

                        input("\nPress Enter to continue...")

                    else:
                        # Invalid result format
                        Config.print_colred("The conversation seems to trail off...", 'warning')
                        return None

                else:
                    Config.print_colored("Invalid choice.", 'error')
                    time.sleep(1)

            except ValueError:
                Config.print_colored("Please enter a number.", 'error')
                time.sleep(1)

    def update_dialogue_state(self, player):
        """Update dialogue state based on player progress"""
        if self.id == "elder_myconid":
            if player.story_progress >= 3 and self.dialogue_state != "late_game":
                self.dialogue_state = "late_game"
            elif "welcome_to_myconaut" in player.completed_quests and self.dialogue_state == "initial":
                self.dialogue_state = "quests"

        elif self.id == "corrupted_druid":
            if player.has_met_elder and self.dialogue_state == "initial":
                self.dialogue_state = "after_elder"
            elif player.story_progress >= 2 and self.dialogue_state != "late_game":
                self.dialogue_state = "late_game"

# NPC definitions
NPCs = {
    "elder_myconid": NPC(
        id="elder_myconid",
        name="Elder Myconid",
        description="The wise leader of the mushroom people. His cap glows with ancient knowledge.",
        art_function=None,
        dialogue_tree={
            "initial": {
                "text": "Welcome, traveler from another world. I am Elder Myconid. Our world is out of balance. Will you help us restore harmony?",
                "options": [
                    ("Tell me more about this world.", "state:explanation"),
                    ("How can I help?", "quest:start"),
                    ("What should I do first?", {"text": "First, gather 3 Glowing Moss samples to prove your commitment. You can find them in the forest.", "next_state": "quests"}),
                    ("Goodbye.", "leave")
                ]
            },
            "explanation": {
                "text": "Long ago, plants and fungi lived in harmony. Then the Corrupted Druid appeared, sowing discord. Now the Root Horror threatens to destroy everything.",
                "options": [
                    ("What should I do?", "state:quests"),
                    ("Who is the Corrupted Druid?", "state:druid_info"),
                    ("Tell me about the Root Horror.", "state:horror_info"),
                    ("Goodbye.", "leave")
                ]
            },
            "quests": {
                "text": "I have several tasks for you. First, gather 3 Glowing Moss from the forest. Then we can discuss the Sporefang menace in the swamp.",
                "options": [
                    ("I accept your quest.", {"text": "Excellent! Return when you have 3 Glowing Moss.", "quest": "start", "next_state": "initial"}),
                    ("Where can I find Glowing Moss?", {"text": "Look in the forest and caves. It glows with a soft blue light.", "next_state": "quests"}),
                    ("I need to prepare first.", "leave")
                ]
            },
            "druid_info": {
                "text": "The Corrupted Druid was once a guardian of the forest. He consumed too much Nightshade and now seeks to destroy all fungi.",
                "options": [
                    ("Where can I find him?", {"text": "He dwells in the Corrupted Grove to the southeast. But be careful, he's dangerous.", "next_state": "initial"}),
                    ("How can he be stopped?", {"text": "Only by restoring balance. You must learn the ways of both plants and fungi.", "next_state": "initial"}),
                    ("Go back.", "state:initial")
                ]
            },
            "horror_info": {
                "text": "The Root Horror is an ancient entity that feeds on discord. It grows stronger as the imbalance worsens.",
                "options": [
                    ("How do I defeat it?", {"text": "You must master alchemy and create the Balance Tincture. Only then can you face it.", "next_state": "initial"}),
                    ("Where is its lair?", {"text": "In the western mountains, in a dark cavern. But don't go there unprepared.", "next_state": "initial"}),
                    ("Go back.", "state:initial")
                ]
            },
            "after_first_quest": {
                "text": "Well done! You've proven yourself. Now, the Sporefang creatures in the swamp have become aggressive. Defeat 5 of them.",
                "options": [
                    ("I'll deal with the Sporefang.", {"text": "Good! Return when the swamp is safe.", "quest": "start", "next_state": "initial"}),
                    ("I need better equipment.", {"text": "Try crafting potions with the alchemy station in your camp.", "next_state": "after_first_quest"}),
                    ("Goodbye.", "leave")
                ]
            },
            "late_game": {
                "text": "You've grown powerful, traveler. The final test awaits. Defeat the Root Horror and restore balance to our world.",
                "options": [
                    ("I'm ready.", {"text": "Then go to the western mountains. May the mycelium guide you.", "quest": "start", "next_state": "initial"}),
                    ("I need to prepare more.", "leave")
                ]
            }
        }
    ),

    "corrupted_druid": NPC(
        id="corrupted_druid",
        name="Corrupted Druid",
        description="A twisted figure covered in thorns and dark vines. His eyes glow with malice.",
        art_function=None,
        dialogue_tree={
            "initial": {
                "text": "Another fungal sympathizer? Leave this place, or be destroyed like the rest!",
                "options": [
                    ("I come in peace.", "state:peace"),
                    ("What happened to you?", "state:story"),
                    ("I'm here to stop you.", "state:threat"),
                    ("Leave.", "leave")
                ]
            },
            "peace": {
                "text": "Peace? There can be no peace while fungi infest our world! They are parasites!",
                "options": [
                    ("Fungi are part of the balance.", {"text": "Balance? *laughs* They consume everything! They must be purged!", "next_state": "initial"}),
                    ("You're the one causing destruction.", "state:threat"),
                    ("I'll leave you to your madness.", "leave")
                ]
            },
            "story": {
                "text": "I consumed the Forbidden Nightshade to gain power against the fungi. Now... now I see the truth! They must all be destroyed!",
                "options": [
                    ("There's another way.", {"text": "No! There is no other way! Only purification by fire!", "next_state": "initial"}),
                    ("You need help.", {"text": "Help? I need no help! I have the power of the plants!", "next_state": "initial"}),
                    ("You're beyond saving.", "state:threat")
                ]
            },
            "threat": {
                "text": "So be it! If you stand with the fungi, you stand against me! Prepare to die!",
                "options": [
                    ("I'll stop you!", {"text": "Then fight! *The druid attacks!*", "trigger": "met_druid", "next_state": "combat"}),
                    ("Wait, let's talk more.", "state:initial")
                ]
            },
            "combat": {
                "text": "*The battle rages...*",
                "options": []
            },
            "after_elder": {
                "text": "So the mushroom-king sent you? He wants to trick you, just as he tricked me!",
                "options": [
                    ("What do you mean?", {"text": "He offers peace but plans to spread his spores everywhere! Don't trust him!", "next_state": "after_elder"}),
                    ("I've seen both sides.", {"text": "Then you must choose! Plants or fungi! There is no middle ground!", "next_state": "after_elder"}),
                    ("I'll make my own choice.", "leave")
                ]
            },
            "late_game": {
                "text": "You've grown stronger... I see the balance in you. Perhaps... perhaps there is another way...",
                "options": [
                    ("There's still time to change.", {"text": "The Nightshade's hold is strong... but... I will consider your words.", "next_state": "initial", "xp": 100}),
                    ("You must atone for your actions.", {"text": "Atonement... yes... perhaps you're right...", "next_state": "initial", "xp": 100}),
                    ("It's too late for you.", {"text": "Then let us finish this! *attacks*", "next_state": "combat"})
                ]
            }
        }
    ),

    "forest_ghost": NPC(
        id="forest_ghost",
        name="Forest Ghost",
        description="A shimmering spirit of a long-dead guardian. It whispers secrets of the forest.",
        art_function=None,
        dialogue_tree={
            "initial": {
                "text": "*whispers* The world is not as it seems... plants and fungi... two sides of the same leaf...",
                "options": [
                    ("What do you mean?", "state:vision"),
                    ("Tell me a secret.", "state:secret"),
                    ("How can I achieve balance?", "state:wisdom"),
                    ("Farewell, spirit.", "leave")
                ]
            },
            "vision": {
                "text": "Consume the Vision Fungus... see the connections... the mycelium network binds all life...",
                "options": [
                    ("Where can I find it?", {"text": "In dark places... where mushrooms grow without light... the caves hold secrets...", "item": "vision_fungus", "next_state": "initial"}),
                    ("What will I see?", "state:prophecy"),
                    ("This sounds dangerous.", "leave")
                ]
            },
            "prophecy": {
                "text": "You will see... three endings... one of balance, one of plants, one of fungi... choose wisely...",
                "options": [
                    ("Tell me about the endings.", "state:endings"),
                    ("How do I find balance?", "state:balance_path"),
                    ("I'm not ready for this.", "leave")
                ]
            },
            "endings": {
                "text": "Balance: unite Elder and Druid... Plant: destroy all fungi... Fungal: consume all plants... the choice is yours...",
                "options": [
                    ("Which is the right path?", {"text": "All paths are right... and wrong... follow your heart...", "next_state": "initial"}),
                    ("How do I unite them?", {"text": "Brew the Balance Tincture... it requires both plant and fungal essence...", "next_state": "initial", "recipe": "balance_tincture_recipe"}),
                    ("This is too much.", "leave")
                ]
            },
            "secret": {
                "text": "The laboratory holds ancient knowledge... the key is in the forest's heart...",
                "options": [
                    ("What key?", {"text": "The Forest Key... craft it from nightshade and sun blossoms...", "next_state": "initial", "recipe": "forest_key_recipe"}),
                    ("Where is the laboratory?", {"text": "North of the village... but locked... you need the key...", "next_state": "initial"}),
                    ("More secrets?", "state:secret2")
                ]
            },
            "secret2": {
                "text": "The Root Horror fears fire... but fire destroys both plant and fungus... be careful...",
                "options": [
                    ("How do I create fire?", {"text": "Sun Blossoms... when crushed with mana caps... create light and heat...", "next_state": "initial"}),
                    ("Thank you, spirit.", {"text": "May balance guide you... *fades away*", "xp": 50, "next_state": "initial"}),
                    ("Goodbye.", "leave")
                ]
            },
            "wisdom": {
                "text": "True balance comes from understanding... not choosing sides... embrace both...",
                "options": [
                    ("How do I embrace both?", {"text": "Learn alchemy... combine plant and fungus... create harmony...", "next_state": "initial"}),
                    ("What if I must choose?", {"text": "Then you have already lost... balance requires no choice... only acceptance...", "next_state": "initial"}),
                    ("I understand.", {"text": "Then you are ready... may your path be true...", "xp": 25, "next_state": "initial"})
                ]
            },
            "balance_path": {
                "text": "Collect all essences... sun and shadow... plant and spore... brew the ultimate tincture...",
                "options": [
                    ("What essences?", {"text": "Sun Blossom, Nightshade, Healing Shroom, Vision Fungus... all four... combined...", "next_state": "initial", "recipe": "balance_tincture_recipe"}),
                    ("Where do I brew it?", {"text": "The ancient laboratory... or your camp with enough skill...", "next_state": "initial"}),
                    ("Thank you.", {"text": "Go in peace... seeker of balance...", "xp": 30, "next_state": "initial"})
                ]
            }
        }
    )
}

def get_npc(npc_id):
    """Get NPC by ID"""
    return NPCs.get(npc_id)
