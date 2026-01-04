#!/bin/bash

# Myconaut - Test Runner Script
# Запуск всех тестов игры

echo "========================================"
echo "     Myconaut - Game Testing Suite      "
echo "========================================"

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "ОШИБКА: Python 3 не установлен"
    exit 1
fi

# Проверка зависимостей
echo "Проверка зависимостей..."
pip3 install colorama --user 2>/dev/null || pip install colorama --user

# Запуск тестов
echo "Запуск тестов..."
echo "========================================"
echo ""

python3 test_game.py

echo ""
echo "========================================"
echo "       Тестирование завершено          "
echo "========================================"
