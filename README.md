# Myconaut

A psychedelic fungal adventure about balance and harmony.

![Myconaut Title](https://img.shields.io/badge/Myconaut-v1.0.0-magenta)
![Python Version](https://img.shields.io/badge/Python-3.8+-blue)
![Platform](https://img.shields.io/badge/Platform-Linux%2FMac-green)

## 🍄 About the Game

Myconaut is a text-based RPG where you explore a world where plants and fungi are at war. As a mycologist transported to a parallel dimension, you must discover the truth about their symbiotic relationship and restore balance to the ecosystem.

**Key Features:**
- Colorful ASCII graphics and psychedelic effects
- Turn-based combat with unique abilities
- Alchemy crafting system with dozens of recipes
- Multiple endings based on your choices
- Password-based save system
- 3-5 hours of gameplay

## 🚀 Installation

### For Linux/Mac:

1. **Clone the repository:**
```bash
git clone https://github.com/mukoningerman/myconaut.git
cd myconaut
```

2. **Make the launch script executable:**
```bash
chmod +x run.sh
```

3. **Run the game:**
```bash
./run.sh
```

### Manual Installation:

1. **Install Python 3.8 or higher**

2. **Install dependencies:**
```bash
pip install colorama
```

3. **Run the game:**
```bash
python3 run.py
# or
python3 src/main.py
```

## 🎮 How to Play

### Controls:
- Use **number keys** (1, 2, 3...) or **letter keys** (N, S, E, W) to choose actions
- Press **Enter** to confirm selections
- Follow on-screen instructions for menus

### Basic Gameplay:
1. **Explore** locations to find resources
2. **Collect** plants and mushrooms
3. **Craft** potions using alchemy
4. **Complete** quests for NPCs
5. **Fight** enemies in turn-based combat
6. **Discover** the story through exploration

### Important Systems:
- **Alchemy**: Combine ingredients to create powerful items
- **Combat**: Strategize with abilities and items
- **Hallucinations**: Some mushrooms alter perception
- **Quests**: Complete tasks for rewards and story progression

## 📁 Project Structure

```
myconaut/
├── src/                    # Source code
│   ├── entities/          # Game entities (items, enemies, NPCs)
│   ├── systems/           # Game systems (combat, alchemy, etc.)
│   ├── world/             # World and locations
│   └── ui/                # User interface
├── data/                  # Game data files
├── saves/                 # Save games (auto-generated)
├── run.py                 # Main launcher
├── run.sh                 # Linux/Mac launcher script
├── config.py              # Configuration
├── requirements.txt       # Dependencies
└── README.md             # This file
```

## 🛠️ Development

### Prerequisites:
- Python 3.8+
- Basic knowledge of Python
- Terminal/Command Line

### Running from source:
```bash
python3 run.py
```

### Modifying the game:
The game is modular and easy to extend:
1. Add new items in `src/entities/item.py`
2. Add new locations in `src/world/location.py`
3. Add new quests in `src/quests.py`
4. Add new NPCs in `src/entities/npc.py`

## 🌟 Features in Detail

### 1. Alchemy System
Combine plants and mushrooms to create:
- Healing potions
- Mana elixirs
- Vision-enhancing brews
- Special keys for locked areas

### 2. Combat System
- Turn-based battles
- Special abilities with mana costs
- Dodging and critical hits
- Enemy special attacks

### 3. Hallucination System
- Visual effects from certain mushrooms
- Altered perception reveals secrets
- Multiple types of hallucinations

### 4. Quest System
- Multiple quest lines
- Different quest types (gather, kill, discover)
- Quest rewards (XP, items, recipes)

### 5. Save System
- Password-based saves
- No files needed to continue game
- Auto-saves to file as backup

## 📜 Story

You are a mycologist who accidentally transports to a parallel world where plants and fungi have sentience and are at war. Guided by the wise Elder Myconid and haunted by the corrupted Druid, you must uncover ancient secrets and make choices that determine the fate of this ecosystem.

**Three possible endings:**
1. **Balance**: Unite plants and fungi in harmony
2. **Plant Dominance**: Help plants eradicate fungi
3. **Fungal Conquest**: Help fungi consume all plants

## 👤 Author

**mukoningerman**
- GitHub: [@mukoningerman](https://github.com/mukoningerman)
- Email: mukonin.german@icloud.com

## 💖 Support

If you enjoy the game, consider supporting development:

**Cryptocurrency Donations:**
- BTC: `bc1qslvfy88nzz99pl8uhdc3v5ynje6qs7csfhveyn`
- ETH: `0xB00541cf0C6745ad24A31c502D6B0BA19d7E8c9A`
- USDT (TRC20): `TTcjEmDYgEwYhE3Qm78rNS6yNnCCj5QYVS`

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Inspired by classic text adventures
- Mycology and botanical studies
- The text adventure community
- All beta testers and contributors

---

**Remember:** Every plant and fungus has its place in the ecosystem. Balance is key.

*"In the world of Myconaut, you are not just a player - you are part of the mycelium network connecting all life."*
