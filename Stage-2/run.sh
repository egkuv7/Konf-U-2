#!/bin/bash
# Скрипт запуска тестов и приложения (этап 2).
cd "$(dirname "$0")" || exit 1
echo "=== Running tests ==="
python3 -m unittest discover -s tests
echo "=== Running application ==="
python3 -m src.main
