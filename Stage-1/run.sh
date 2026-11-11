#!/bin/bash
# Скрипт для запуска тестов и приложения.
echo "=== Running tests ==="
python3 -m unittest discover -s tests
echo "=== Running application ==="
python3 -m src.main
