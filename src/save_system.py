"""
Myconaut - Save System using Password Codes
"""

from config import Config
import base64
import json
import hashlib
import zlib
import os

class SaveSystem:
    """Handles game saving and loading via password codes"""

    def __init__(self):
        self.save_dir = Config.SAVE_DIR

        # Create save directory if it doesn't exist
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def generate_password(self, game_state):
        """Generate a password code from game state"""
        try:
            # Convert game state to JSON string
            state_json = json.dumps(game_state, separators=(',', ':'))

            # Compress the data
            compressed = zlib.compress(state_json.encode('utf-8'), level=9)

            # Add checksum
            checksum = hashlib.md5(compressed).hexdigest()[:4]
            data_with_checksum = checksum.encode() + compressed

            # Encode with base64
            encoded = base64.b64encode(data_with_checksum)

            # Convert to readable password (remove padding, group)
            password = encoded.decode('ascii').replace('=', '')
            password = '-'.join([password[i:i+4] for i in range(0, len(password), 4)])

            return password

        except Exception as e:
            Config.print_colored(f"Error generating password: {e}", 'error')
            return None

    def decode_password(self, password):
        """Decode password code to game state with better error handling"""
        try:
            # Remove hyphens and add padding if needed
            clean_password = password.replace('-', '')

            # Add padding if necessary
            padding = 4 - (len(clean_password) % 4)
            if padding != 4:
                clean_password += '=' * padding

            # Decode from base64
            decoded = base64.b64decode(clean_password)

            # Verify checksum
            checksum = decoded[:4].decode('ascii', errors='ignore')
            compressed_data = decoded[4:]

            calculated_checksum = hashlib.md5(compressed_data).hexdigest()[:4]
            if checksum != calculated_checksum:
                Config.print_colored("Invalid password: checksum mismatch", 'error')
                return None

            # Decompress
            decompressed = zlib.decompress(compressed_data)

            # Parse JSON
            game_state = json.loads(decompressed.decode('utf-8'))

            # Ensure all data is properly formatted
            game_state = self.fix_save_data(game_state)

            return game_state

        except Exception as e:
            Config.print_colored(f"Error decoding password: {e}", 'error')
            return None

    def fix_save_data(self, game_state):
        """Fix common issues in save data"""
        if 'player' in game_state:
            player_data = game_state['player']

            # Ensure visited_locations is a list of lists
            if 'visited_locations' in player_data:
                visited = player_data['visited_locations']
                if isinstance(visited, list):
                    fixed_visited = []
                    for loc in visited:
                        if isinstance(loc, tuple):
                            fixed_visited.append(list(loc))
                        elif isinstance(loc, list):
                            fixed_visited.append(loc)
                        else:
                            # Try to convert
                            try:
                                fixed_visited.append(list(loc))
                            except:
                                fixed_visited.append([0, 0])
                    player_data['visited_locations'] = fixed_visited

            # Ensure current_location is a list
            if 'current_location' in player_data:
                loc = player_data['current_location']
                if isinstance(loc, tuple):
                    player_data['current_location'] = list(loc)
                elif not isinstance(loc, list):
                    player_data['current_location'] = [2, 2]  # Default start

        return game_state

    def save_game(self, player, game):
        """Save game and return password"""
        game_state = {
            'player': player.save_data(),
            'game': game.save_data(),
            'version': Config.VERSION,
            'timestamp': time.time()
        }

        password = self.generate_password(game_state)

        if password:
            # Also save to file for convenience
            filename = f"{self.save_dir}/save_{int(time.time())}.mcs"
            with open(filename, 'w') as f:
                json.dump(game_state, f)

            Config.print_colored("\n╔══════════════════════════════════════════════════════════════════════╗", 'title')
            Config.print_colored("║                         GAME SAVED!                                 ║", 'title')
            Config.print_colored("╠══════════════════════════════════════════════════════════════════════╣", 'title')
            Config.print_colored(f"║ Password: {password:^64} ║", 'highlight')
            Config.print_colored("╚══════════════════════════════════════════════════════════════════════╝", 'title')
            Config.print_colored("\nWrite down this password to continue your adventure later!", 'info')
            Config.print_colored("You can also find a backup save in the 'saves' folder.", 'info')

        return password

    def load_game(self, password):
        """Load game from password with better error handling"""
        game_state = self.decode_password(password)

        if not game_state:
            Config.print_colored("Failed to decode password!", 'error')
            return None, None

        # Check version compatibility
        if game_state.get('version') != Config.VERSION:
            Config.print_colored(f"Warning: Save version {game_state.get('version')} may not be compatible with game version {Config.VERSION}", 'warning')

        return game_state.get('player'), game_state.get('game')

    def save_to_file(self, filename, game_state):
        """Save game state to file"""
        try:
            with open(f"{self.save_dir}/{filename}", 'w') as f:
                json.dump(game_state, f)
            return True
        except Exception as e:
            Config.print_colored(f"Error saving to file: {e}", 'error')
            return False

    def load_from_file(self, filename):
        """Load game state from file"""
        try:
            with open(f"{self.save_dir}/{filename}", 'r') as f:
                game_state = json.load(f)
            return game_state.get('player'), game_state.get('game')
        except Exception as e:
            Config.print_colored(f"Error loading from file: {e}", 'error')
            return None, None

# Import time here to avoid circular import
import time
