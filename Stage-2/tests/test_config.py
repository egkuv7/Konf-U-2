"""Тесты модуля конфигурации."""
import json
import os
import unittest

from src.config import load_config, validate_config


class TestConfig(unittest.TestCase):
    """Тесты функций загрузки и проверки конфигурации."""

    TEST_FILE = "test_config.json"

    def setUp(self):
        """Создать файл с корректной конфигурацией."""
        self.valid_data = {
            "package_name": "curl",
            "repo_url": "tests/mock_packages.txt",
            "test_mode": True,
            "package_version": "7.81.0-1ubuntu1.16",
            "output_image_name": "graph.svg",
            "ascii_tree_mode": False,
            "filter_substring": "lib",
        }
        with open(self.TEST_FILE, "w", encoding="utf-8") as file:
            json.dump(self.valid_data, file)

    def tearDown(self):
        """Удалить временный файл конфигурации."""
        if os.path.exists(self.TEST_FILE):
            os.remove(self.TEST_FILE)

    def test_load_valid_config(self):
        """Корректный JSON загружается без ошибок."""
        config = load_config(self.TEST_FILE)
        self.assertEqual(config["package_name"], "curl")

    def test_load_missing_file(self):
        """Отсутствующий файл вызывает FileNotFoundError."""
        with self.assertRaises(FileNotFoundError):
            load_config("nonexistent.json")

    def test_validate_valid_config(self):
        """Корректная конфигурация проходит проверку."""
        self.assertTrue(validate_config(self.valid_data))

    def test_validate_missing_field(self):
        """Отсутствующее поле вызывает KeyError."""
        data = self.valid_data.copy()
        data.pop("package_name")
        with self.assertRaises(KeyError):
            validate_config(data)

    def test_validate_wrong_type(self):
        """Неверный тип поля вызывает TypeError."""
        data = self.valid_data.copy()
        data["test_mode"] = "yes"
        with self.assertRaises(TypeError):
            validate_config(data)

    def test_validate_empty_string(self):
        """Пустая строка в обязательном поле вызывает ValueError."""
        data = self.valid_data.copy()
        data["package_name"] = "   "
        with self.assertRaises(ValueError):
            validate_config(data)

    def test_validate_bad_image_extension(self):
        """Неподдерживаемое расширение вызывает ValueError."""
        data = self.valid_data.copy()
        data["output_image_name"] = "graph.bmp"
        with self.assertRaises(ValueError):
            validate_config(data)
