"""
Myconaut - Hallucination System
"""

from config import Config
import random
import time
import sys

class HallucinationEffect:
    """Base hallucination effect"""

    def __init__(self, name, description, duration=5):
        self.name = name
        self.description = description
        self.duration = duration  # in turns
        self.active = False
        self.turns_left = duration

    def activate(self):
        """Activate the effect"""
        self.active = True
        self.turns_left = self.duration
        Config.print_colored(f"\n{self.description}", 'magic')

    def update(self, game):
        """Update effect each turn"""
        if not self.active:
            return

        self.turns_left -= 1
        if self.turns_left <= 0:
            self.deactivate(game)
            return

        # Apply effect
        self.apply_effect(game)

    def apply_effect(self, game):
        """Apply the specific effect"""
        pass

    def deactivate(self, game):
        """Deactivate the effect"""
        self.active = False
        Config.print_colored(f"\nThe {self.name} effect fades away.", 'normal')

    def modify_text(self, text):
        """Modify text output based on effect"""
        return text

class ColorShiftEffect(HallucinationEffect):
    """Shifts colors randomly"""

    def __init__(self):
        super().__init__("Color Shift", "Colors dance and shift before your eyes...")

    def apply_effect(self, game):
        """Shift color output"""
        # This effect is handled in the display system
        pass

    def modify_text(self, text):
        """Add random color codes to text"""
        colors = [Config.COLORS['magic'], Config.COLORS['plant'],
                 Config.COLORS['mushroom'], Config.COLORS['info']]
        colored_text = ""
        for char in text:
            if random.random() < 0.1:  # 10% chance to color each character
                colored_text += random.choice(colors) + char + Config.COLORS['normal']
            else:
                colored_text += char
        return colored_text

class WhisperingEffect(HallucinationEffect):
    """Hear whispering voices"""

    def __init__(self):
        super().__init__("Whispering Voices", "You hear whispers from the plants and fungi...")

    def apply_effect(self, game):
        """Occasionally print whispers"""
        if random.random() < 0.3:  # 30% chance per turn
            whispers = [
                "The mycelium knows...",
                "Balance is key...",
                "The roots speak of secrets...",
                "Fungi are friends, not food...",
                "The druid sees only half the truth...",
                "Consume the vision... see the connections..."
            ]
            whisper = random.choice(whispers)
            Config.print_colored(f"\n*whisper* {whisper}", 'magic')

class VisualDistortionEffect(HallucinationEffect):
    """Visual distortion effects"""

    def __init__(self):
        super().__init__("Visual Distortion", "Reality bends and twists around you...")

    def apply_effect(self, game):
        """Apply visual distortions"""
        if random.random() < 0.4:  # 40% chance per turn
            distortions = [
                "\nThe walls seem to breathe...",
                "\nShadows move on their own...",
                "\nColors bleed into each other...",
                "\nPatterns emerge from nothingness..."
            ]
            distortion = random.choice(distortions)
            print(Config.COLORS['magic'] + distortion + Config.COLORS['normal'])

class EnhancedVisionEffect(HallucinationEffect):
    """See hidden things"""

    def __init__(self):
        super().__init__("Enhanced Vision", "You see connections and hidden paths...")

    def apply_effect(self, game):
        """Reveal hidden information"""
        # This effect reveals additional options or information
        pass

class HallucinationManager:
    """Manages hallucination effects"""

    def __init__(self):
        self.active_effects = []
        self.effect_pool = {
            "color_shift": ColorShiftEffect(),
            "whispering": WhisperingEffect(),
            "visual_distortion": VisualDistortionEffect(),
            "enhanced_vision": EnhancedVisionEffect()
        }

    def add_effect(self, effect_name):
        """Add a hallucination effect"""
        if effect_name in self.effect_pool:
            effect = self.effect_pool[effect_name]
            effect.activate()
            self.active_effects.append(effect)
            return True
        return False

    def remove_effect(self, effect_name):
        """Remove a hallucination effect"""
        self.active_effects = [e for e in self.active_effects if e.name != effect_name]

    def update(self, game):
        """Update all active effects"""
        for effect in self.active_effects[:]:  # Copy list for safe removal
            effect.update(game)
            if not effect.active:
                self.active_effects.remove(effect)

    def modify_output(self, text):
        """Modify text output based on active effects"""
        modified_text = text
        for effect in self.active_effects:
            modified_text = effect.modify_text(modified_text)
        return modified_text

    def has_effect(self, effect_name):
        """Check if effect is active"""
        return any(e.name == effect_name for e in self.active_effects)

    def clear_all(self):
        """Clear all hallucination effects"""
        self.active_effects.clear()

    def get_active_effects_names(self):
        """Get names of active effects"""
        return [e.name for e in self.active_effects]
