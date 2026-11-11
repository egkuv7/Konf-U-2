"""Тесты для модуля конфигурации."""
import json
import os
import unittest
from src.config import load_config, validate_config


class TestConfig(unittest.TestCase):
    """Тестовый пример для функций конфигурации."""

    TEST_FILE = "test_config.json"

    def setUp(self):
        """Настроить фикстуру с допустимой конфигурацией."""
        self.valid_data = {
            "package_name": "curl",
            "repo_url": "http://example.com/Packages.gz",
            "test_mode": True,
            "package_version": "7.81.0-1",
            "output_image_name": "graph.png",
            "ascii_tree_mode": False,
            "filter_substring": "lib",
        }
        with open(self.TEST_FILE, "w", encoding="utf-8") as f:
            json.dump(self.valid_data, f)

    def tearDown(self):
        """Удалить файл тестового фикстура."""
        if os.path.exists(self.TEST_FILE):
            os.remove(self.TEST_FILE)

    def test_load_valid_config(self):
        """Тест загрузки корректной конфигурации в формате JSON."""
        config = load_config(self.TEST_FILE)
        self.assertEqual(config["package_name"], "curl")

    def test_load_missing_file(self):
        """Ошибка при тестировании, если файл отсутствует."""
        with self.assertRaises(FileNotFoundError):
            load_config("nonexistent.json")

    def test_validate_valid_config(self):
        """Проверка правильности конфигурации."""
        result = validate_config(self.valid_data)
        self.assertTrue(result)

    def test_validate_missing_field(self):
        """Ошибка теста при отсутствии обязательного поля."""
        data = self.valid_data.copy()
        data.pop("package_name")
        with self.assertRaises(KeyError):
            validate_config(data)

    def test_validate_wrong_type(self):
        """Ошибка при проверке, если поле имеет неверный тип."""
        data = self.valid_data.copy()
        data["test_mode"] = "yes"
        with self.assertRaises(TypeError):
            validate_config(data)

    def test_validate_empty_string(self):
        """Ошибка теста, когда требуемая строка пуста."""
        data = self.valid_data.copy()
        data["package_name"] = "   "
        with self.assertRaises(ValueError):
            validate_config(data)

    def test_validate_bad_image_extension(self):
        """Ошибка при тестировании неподдерживаемого расширения изображения."""
        data = self.valid_data.copy()
        data["output_image_name"] = "graph.bmp"
        with self.assertRaises(ValueError):
            validate_config(data)
