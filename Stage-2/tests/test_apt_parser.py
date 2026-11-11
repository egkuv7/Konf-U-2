"""Тесты парсера индекса Packages (apt)."""
import os
import unittest

from src.apt_parser import clean_name, fetch_index, find_package
from src.apt_parser import parse_depends, parse_fields

MOCK_FILE = os.path.join(
    os.path.dirname(__file__), "mock_packages.txt"
)


class TestAptParser(unittest.TestCase):
    """Тесты функций разбора индекса репозитория."""

    def setUp(self):
        """Загрузить текст тестового репозитория."""
        with open(MOCK_FILE, "r", encoding="utf-8") as file:
            self.text = file.read()

    def test_clean_name_with_version(self):
        """Имя очищается от ограничения версии."""
        self.assertEqual(clean_name("libc6 (>= 2.34)"), "libc6")

    def test_clean_name_with_arch(self):
        """Имя очищается от суффикса архитектуры."""
        self.assertEqual(clean_name("libc6:any"), "libc6")

    def test_parse_depends_simple(self):
        """Простой список зависимостей разбирается по запятым."""
        deps = parse_depends("libc6 (>= 2.34), zlib1g")
        self.assertEqual(deps, ["libc6", "zlib1g"])

    def test_parse_depends_alternatives(self):
        """Альтернативы сохраняются в одной группе."""
        deps = parse_depends("debconf (>= 0.5) | debconf-2.0")
        self.assertEqual(deps, ["debconf | debconf-2.0"])

    def test_parse_depends_empty(self):
        """Пустое поле Depends даёт пустой список."""
        self.assertEqual(parse_depends(""), [])

    def test_parse_fields_continuation(self):
        """Многострочное поле Depends склеивается в одну строку."""
        stanza = "Package: x\nDepends: a,\n b\n"
        fields = parse_fields(stanza)
        self.assertEqual(fields["Depends"], "a, b")

    def test_find_package_by_version(self):
        """Пакет находится по точному имени и версии."""
        fields = find_package(self.text, "curl", "7.81.0-1ubuntu1.16")
        self.assertEqual(fields["Package"], "curl")

    def test_find_package_wrong_version(self):
        """Несовпадение версии даёт None."""
        self.assertIsNone(find_package(self.text, "curl", "0.0"))

    def test_fetch_index_test_mode(self):
        """В тестовом режиме индекс читается из файла."""
        text = fetch_index(MOCK_FILE, True)
        self.assertIn("Package: curl", text)

    def test_package_without_depends(self):
        """Пакет без поля Depends не имеет зависимостей."""
        fields = find_package(self.text, "coreutils", "8.32-4.1ubuntu1")
        deps = parse_depends(fields.get("Depends", ""))
        self.assertEqual(deps, [])
