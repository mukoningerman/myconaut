#!/usr/bin/env python3
"""
Myconaut - Game Tester
Комплексный тест всех систем игры
"""

import sys
import os

# Добавляем пути для импортов
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

def run_all_tests():
    """Запуск всех тестов"""
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║                    MYCONAUT - SYSTEM TESTER                         ║")
    print("╠══════════════════════════════════════════════════════════════════════╣")

    tests = [
        test_imports,
        test_config,
        test_ascii_art,
        test_items,
        test_inventory,
        test_enemies,
        test_locations,
        test_player,
        test_quests,
        test_npc,
        test_alchemy,
        test_save_system,
        test_combat_basics,
        test_game_initialization
    ]

    passed = 0
    failed = 0

    for test in tests:
        print(f"\n{'='*60}")
        print(f"Running: {test.__name__}")
        print(f"{'='*60}")
        try:
            test()
            print(f"✓ {test.__name__}: PASSED")
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__}: FAILED - {e}")
            failed += 1
        except:
            print(f"✗ {test.__name__}: FAILED - Unknown error")
            failed += 1

    print("\n" + "="*80)
    print("TEST SUMMARY:")
    print(f"  Passed: {passed}/{len(tests)}")
    print(f"  Failed: {failed}/{len(tests)}")
    print("="*80)

    if failed == 0:
        print("\n🎉 Все тесты пройдены! Игра готова к запуску!")
        return True
    else:
        print("\n⚠️  Некоторые тесты не прошли. Проверьте ошибки выше.")
        return False

def test_imports():
    """Тест импортов всех модулей"""
    modules = [
        'config',
        'ascii_art',
        'player',
        'entities.item',
        'entities.enemy',
        'entities.npc',
        'world.location',
        'quests',
        'alchemy',
        'combat',
        'save_system',
        'systems.hallucination_system'
    ]

    for module in modules:
        try:
            __import__(module)
        except ImportError as e:
            raise ImportError(f"Не удалось импортировать {module}: {e}")

def test_config():
    """Тест конфигурации"""
    from config import Config

    assert Config.GAME_NAME == "Myconaut"
    assert Config.VERSION == "1.0.0"
    assert Config.AUTHOR == "mukoningerman"

    # Проверка цветов
    assert 'title' in Config.COLORS
    assert 'normal' in Config.COLORS
    assert 'error' in Config.COLORS
    assert 'success' in Config.COLORS

    print(f"  Game: {Config.GAME_NAME} v{Config.VERSION}")
    print(f"  Author: {Config.AUTHOR}")
    print(f"  Colors configured: {len(Config.COLORS)}")

def test_ascii_art():
    """Тест ASCII графики"""
    from ascii_art import ASCIIArt

    # Проверка существования методов
    title = ASCIIArt.title_screen()
    assert isinstance(title, str)
    assert len(title) > 0

    forest = ASCIIArt.forest()
    assert isinstance(forest, str)

    cave = ASCIIArt.cave()
    assert isinstance(cave, str)

    player_art = ASCIIArt.player()
    assert isinstance(player_art, str)

    print(f"  Title screen generated: {len(title)} chars")
    print(f"  Forest art generated")
    print(f"  Player art generated")

def test_items():
    """Тест системы предметов"""
    try:
        # Проверяем, что модуль загружается
        import entities.item as item_module
        print(f"  ✓ Модуль entities.item загружен")

        # Проверяем основные классы
        assert hasattr(item_module, 'Item'), "Класс Item не найден"
        assert hasattr(item_module, 'ItemType'), "Enum ItemType не найден"
        assert hasattr(item_module, 'Rarity'), "Enum Rarity не найден"
        assert hasattr(item_module, 'Inventory'), "Класс Inventory не найден"
        assert hasattr(item_module, 'create_item'), "Функция create_item не найдена"

        print(f"  ✓ Основные классы и функции найдены")

        # Проверка существования ITEMS
        if not hasattr(item_module, 'ITEMS'):
            print(f"  ⚠️ ITEMS не найден как атрибут модуля")
            # Проверяем, есть ли ITEMS в глобальной области видимости
            import sys
            module_name = item_module.__name__
            if 'ITEMS' in sys.modules[module_name].__dict__:
                ITEMS = sys.modules[module_name].__dict__['ITEMS']
            else:
                raise AssertionError("ITEMS не найден в модуле")
        else:
            ITEMS = item_module.ITEMS

        print(f"  ✓ ITEMS найден, содержит {len(ITEMS)} предметов")

        # Проверка базовых предметов
        required_items = ['glowing_moss', 'healing_shroom', 'mana_cap', 'vision_fungus']
        for item_id in required_items:
            if item_id in ITEMS:
                print(f"  ✓ Предмет '{item_id}' найден в базе данных")
            else:
                raise AssertionError(f"Предмет '{item_id}' отсутствует в базе данных")

        # Создание предмета
        moss = item_module.create_item('glowing_moss')
        assert moss is not None, "Не удалось создать предмет 'glowing_moss'"
        print(f"  ✓ Предмет 'glowing_moss' создан")

        assert moss.name == "Glowing Moss", f"Некорректное имя: {moss.name}"
        assert moss.type == item_module.ItemType.PLANT, f"Некорректный тип: {moss.type}"

        # ПРАВИЛЬНАЯ ПРОВЕРКА: эффект находится в ключе 'effect' словаря effects
        assert 'effect' in moss.effects, f"В effects должен быть ключ 'effect'. Effects: {moss.effects}"
        assert moss.effects['effect'] == 'mana', f"Эффект должен быть 'mana', а получен: {moss.effects.get('effect')}"
        print(f"  ✓ Эффекты предмета корректны: {moss.effects}")

        shroom = item_module.create_item('healing_shroom')
        assert shroom is not None, "Не удалось создать предмет 'healing_shroom'"
        print(f"  ✓ Предмет 'healing_shroom' создан")
        assert shroom.effects['effect'] == 'heal', f"Эффект должен быть 'heal', а получен: {shroom.effects.get('effect')}"

        # Проверяем другие важные предметы
        vision = item_module.create_item('vision_fungus')
        assert vision is not None, "Не удалось создать предмет 'vision_fungus'"
        assert vision.effects['effect'] == 'hallucination', f"Эффект должен быть 'hallucination'"

        mana_cap = item_module.create_item('mana_cap')
        assert mana_cap is not None, "Не удалось создать предмет 'mana_cap'"
        assert mana_cap.effects['effect'] == 'mana', f"Эффект должен быть 'mana'"

        print(f"  Итого предметов в базе: {len(ITEMS)}")
        print(f"  Пример предмета: {moss.name} ({moss.type.value}) - {moss.description}")

    except ImportError as e:
        print(f"  ✗ Ошибка импорта: {e}")
        # Показать содержимое директории
        import os
        entities_dir = os.path.join(os.path.dirname(__file__), 'src', 'entities')
        if os.path.exists(entities_dir):
            print(f"  Содержимое директории entities: {os.listdir(entities_dir)}")
        raise
    except Exception as e:
        print(f"  ✗ Ошибка во время теста: {e}")
        import traceback
        traceback.print_exc()
        raise

def quick_playtest():
    """Быстрая проверка игрового процесса"""
    print("\n" + "="*80)
    print("QUICK PLAYTEST - Проверка основных игровых механик")
    print("="*80)

    try:
        from game import Game

        game = Game()
        game.start_new_game()

        # Проверка начального состояния
        assert game.player is not None
        assert len(game.player.inventory.items) > 0

        # Проверяем, что игрок получил стартовые предметы
        print(f"  Стартовые предметы: {len(game.player.inventory.items)}")
        for item_id, item in game.player.inventory.items.items():
            print(f"    - {item.name} x{item.quantity}")

        # В начале игры квесты могут не стартовать автоматически
        # Проверяем, что система квестов инициализирована
        assert game.quest_manager is not None

        # Если есть NPC в стартовой локации, то квесты могут быть доступны
        from world.location import get_location
        loc = get_location(*game.player.current_location)
        assert loc is not None

        print("✓ Новая игра успешно создана")
        print(f"  Игрок: {game.player.name}")
        print(f"  Стартовая локация: {loc.name}")
        print(f"  Стартовые предметы: {len(game.player.inventory.items)}")
        print(f"  Активные квесты: {len(game.player.active_quests)}")
        print(f"  Квесты доступны: {len(game.quest_manager.get_available_quests())}")

        # Проверка движений
        available_directions = loc.get_available_directions()
        print(f"  Доступные направления: {[d[1] for d in available_directions]}")

        # Быстрая проверка NPC
        if loc.npcs:
            from entities.npc import get_npc
            for npc_id in loc.npcs:
                npc = get_npc(npc_id)
                if npc:
                    print(f"  NPC в локации: {npc.name}")

        # Проверяем, что игрок может получать квесты
        # Для этого нужно пойти в деревню (2, 1) и поговорить с Elder Myconid
        print(f"\n  Совет: Для получения квестов идите в Myconid Village (North)")

        return True

    except Exception as e:
        print(f"✗ Ошибка в быстрой проверке: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_inventory():
    """Тест инвентаря"""
    from entities.item import Inventory, create_item

    inv = Inventory(max_size=20)

    # Добавление предметов
    moss = create_item('glowing_moss')
    shroom = create_item('healing_shroom')

    assert inv.add_item(moss, 3) == True
    assert inv.add_item(shroom, 2) == True

    # Проверка наличия
    assert inv.has_item('glowing_moss', 2) == True
    assert inv.has_item('glowing_moss', 5) == False

    # Удаление
    assert inv.remove_item('glowing_moss', 1) == True
    assert inv.has_item('glowing_moss', 2) == True

    print(f"  Inventory capacity: {inv.max_size}")
    print(f"  Items in inventory: {len(inv.items)}")

def test_enemies():
    """Тест системы врагов"""
    from entities.enemy import create_enemy, ENEMIES

    # Проверка существования врагов
    assert 'sporefang' in ENEMIES
    assert 'thornbeast' in ENEMIES
    assert 'mindshroom' in ENEMIES
    assert 'root_horror' in ENEMIES

    # Создание врага
    enemy = create_enemy('sporefang')
    assert enemy is not None
    assert enemy.name == "Sporefang"
    assert enemy.health > 0
    assert enemy.damage > 0

    # Тест получения урона
    initial_health = enemy.health
    damage_taken = enemy.take_damage(10)
    assert enemy.health == initial_health - 10
    assert damage_taken == 10

    print(f"  Enemies in database: {len(ENEMIES)}")
    print(f"  Sample enemy: {enemy.name} (HP: {enemy.health}, DMG: {enemy.damage})")

def test_locations():
    """Тест системы локаций"""
    from world.location import get_location, Location, LocationType

    # Получение стартовой локации
    loc = get_location(2, 2)
    assert loc is not None
    assert loc.name == "Whispering Forest Clearing"
    assert loc.type == LocationType.FOREST

    # Проверка соединений
    connections = loc.connections
    assert 'n' in connections
    assert 's' in connections
    assert 'e' in connections
    assert 'w' in connections

    # Проверка ресурсов
    assert len(loc.items) > 0

    # Исследование
    found_items = loc.explore()
    assert isinstance(found_items, list)

    print(f"  Start location: {loc.name}")
    print(f"  Connections: {len(loc.connections)} directions")
    print(f"  Available items: {len(loc.items)} types")

def test_player():
    """Тест системы игрока"""
    from player import Player

    player = Player("TestPlayer")

    # Базовая проверка
    assert player.name == "TestPlayer"
    assert player.level == 1
    assert player.health > 0
    assert player.mana > 0

    # Тест получения урона
    initial_health = player.health
    damage = player.take_damage(20)
    assert player.health == initial_health - damage

    # Тест лечения
    player.heal(10)
    assert player.health > initial_health - damage

    # Тест получения опыта
    initial_xp = player.xp
    player.add_xp(50)
    assert player.xp == initial_xp + 50

    # Тест инвентаря
    assert player.inventory is not None

    print(f"  Player: {player.name} (Level {player.level})")
    print(f"  Stats: HP={player.health}, MP={player.mana}, DMG={player.base_damage}")
    print(f"  Inventory size: {player.inventory.max_size}")

def test_quests():
    """Тест системы квестов"""
    from quests import Quest, QuestType, QuestStatus, QuestManager, QUESTS
    from player import Player

    # Проверка квестов в базе данных
    assert 'welcome_to_myconaut' in QUESTS
    assert 'sporefang_menace' in QUESTS
    assert 'lost_laboratory' in QUESTS

    # Создание игрока и менеджера квестов
    player = Player("TestPlayer")
    quest_manager = QuestManager(player)

    # Доступные квесты
    available = quest_manager.get_available_quests()
    assert len(available) > 0

    # Старт квеста
    quest = QUESTS['welcome_to_myconaut']
    assert quest.start(player) == True
    assert quest.id in player.active_quests

    print(f"  Quests in database: {len(QUESTS)}")
    print(f"  Available quests: {len(available)}")
    print(f"  Sample quest: {quest.name}")

def test_npc():
    """Тест системы NPC"""
    from entities.npc import get_npc, NPCs

    # Проверка NPC в базе данных
    assert 'elder_myconid' in NPCs
    assert 'corrupted_druid' in NPCs
    assert 'forest_ghost' in NPCs

    # Получение NPC
    elder = get_npc('elder_myconid')
    assert elder is not None
    assert elder.name == "Elder Myconid"
    assert elder.id == "elder_myconid"

    # Проверка диалогового дерева
    assert 'initial' in elder.dialogue_tree
    assert 'text' in elder.dialogue_tree['initial']
    assert 'options' in elder.dialogue_tree['initial']

    print(f"  NPCs in database: {len(NPCs)}")
    print(f"  Sample NPC: {elder.name}")

def test_alchemy():
    """Тест системы алхимии"""
    from alchemy import RECIPES, Recipe
    from player import Player

    # Проверка рецептов
    assert 'health_potion_recipe' in RECIPES
    assert 'mana_elixir_recipe' in RECIPES
    assert 'vision_potion_recipe' in RECIPES

    # Проверка игрока
    player = Player("TestPlayer")
    player.add_recipe('health_potion_recipe')

    assert 'health_potion_recipe' in player.discovered_recipes

    print(f"  Recipes in database: {len(RECIPES)}")
    print(f"  Player knows recipes: {len(player.discovered_recipes)}")

def test_save_system():
    """Тест системы сохранения"""
    from save_system import SaveSystem
    from player import Player

    player = Player("TestPlayer")
    save_system = SaveSystem()

    # Тестовые данные
    test_state = {
        'player': player.save_data(),
        'game': {'current_turn': 5, 'game_start_time': 1234567890},
        'version': '1.0.0',
        'timestamp': 1234567890
    }

    # Генерация пароля
    password = save_system.generate_password(test_state)
    assert password is not None
    assert isinstance(password, str)
    assert len(password) > 10

    # Декодирование пароля
    decoded_state = save_system.decode_password(password)
    assert decoded_state is not None
    assert decoded_state['version'] == '1.0.0'

    print(f"  Save system initialized")
    print(f"  Password generated: {password[:20]}...")
    print(f"  Password decoded successfully")

def test_combat_basics():
    """Тест базовой системы боя"""
    from combat import Combat
    from player import Player

    player = Player("TestPlayer")

    # Увеличим здоровье для теста
    player.health = 100
    player.max_health = 100

    # Создаем тестовый бой
    combat = Combat(player, 'sporefang')

    assert combat.player == player
    assert combat.enemy is not None
    assert combat.enemy.name == "Sporefang"
    assert combat.combat_active == True

    print(f"  Combat system initialized")
    print(f"  Player vs {combat.enemy.name}")
    print(f"  Enemy HP: {combat.enemy.health}")

def test_game_initialization():
    """Тест инициализации игры"""
    from game import Game

    game = Game()
    assert game is not None
    assert game.player is None
    assert game.quest_manager is None
    assert game.game_running == False

    # Инициализация новой игры (без запуска главного цикла)
    game.start_new_game()

    # После старта игры должен быть создан игрок
    assert game.player is not None
    assert isinstance(game.player.name, str)

    print(f"  Game initialized")
    print(f"  Player created: {game.player.name}")

def quick_playtest():
    """Быстрая проверка игрового процесса"""
    print("\n" + "="*80)
    print("QUICK PLAYTEST - Проверка основных игровых механик")
    print("="*80)

    try:
        from game import Game

        game = Game()
        game.start_new_game()

        # Проверка начального состояния
        assert game.player is not None
        assert len(game.player.inventory.items) > 0

        # Игра может не стартовать квесты сразу, только после разговора с NPC
        # Вместо этого проверяем, что система квестов инициализирована
        assert game.quest_manager is not None
        assert hasattr(game.player, 'completed_quests')
        assert hasattr(game.player, 'active_quests')

        # Проверка стартовой локации
        from world.location import get_location
        loc = get_location(*game.player.current_location)
        assert loc is not None

        print("✓ Новая игра успешно создана")
        print(f"  Игрок: {game.player.name}")
        print(f"  Стартовая локация: {loc.name}")
        print(f"  Стартовые предметы: {len(game.player.inventory.items)}")
        print(f"  Активные квесты: {len(game.player.active_quests)}")
        print(f"  Квесты доступны: {len(game.quest_manager.get_available_quests())}")

        # Проверка движений
        available_directions = loc.get_available_directions()
        print(f"  Доступные направления: {[d[1] for d in available_directions]}")

        # Быстрая проверка NPC
        if loc.npcs:
            from entities.npc import get_npc
            for npc_id in loc.npcs:
                npc = get_npc(npc_id)
                if npc:
                    print(f"  NPC в локации: {npc.name}")

        return True

    except Exception as e:
        print(f"✗ Ошибка в быстрой проверке: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Главная функция тестирования"""
    print("\n" + "="*80)
    print("MYCONAUT - ПОЛНЫЙ ТЕСТ ИГРОВЫХ СИСТЕМ")
    print("="*80)

    print("\nЭтап 1: Тестирование отдельных модулей...")
    modules_ok = run_all_tests()

    print("\nЭтап 2: Быстрая проверка игрового процесса...")
    gameplay_ok = quick_playtest()

    print("\n" + "="*80)
    print("ИТОГОВЫЙ ОТЧЕТ:")
    print("="*80)

    if modules_ok and gameplay_ok:
        print("\n✅ ВСЕ СИСТЕМЫ РАБОТАЮТ КОРРЕКТНО!")
        print("\nИгра готова к запуску. Вы можете:")
        print("1. Запустить игру: python3 run.py")
        print("2. Или использовать скрипт: ./run.sh")
        print("\nУдачи в приключении, Myconaut! 🍄")
        return 0
    else:
        print("\n⚠️  ОБНАРУЖЕНЫ ПРОБЛЕМЫ!")
        print("\nЧто делать:")
        print("1. Проверьте структуру проекта")
        print("2. Убедитесь, что все файлы на месте")
        print("3. Проверьте импорты в модулях")
        print("4. Запустите отдельные тесты для выявления проблемы")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nТестирование прервано пользователем.")
        sys.exit(1)
    except Exception as e:
        print(f"\nКритическая ошибка при тестировании: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(2)
