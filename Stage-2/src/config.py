"""Модуль загрузки и проверки конфигурации (этап 2)."""
import json
import os

CONFIG_FILE = "config.json"

REQUIRED_FIELDS = {
    "package_name": str,
    "repo_url": str,
    "test_mode": bool,
    "package_version": str,
    "output_image_name": str,
    "ascii_tree_mode": bool,
    "filter_substring": str,
}

NON_EMPTY_STRING_FIELDS = {
    "package_name",
    "repo_url",
    "package_version",
    "output_image_name",
}

IMAGE_EXTENSIONS = {".png", ".svg", ".jpg", ".jpeg"}


def load_config(file_path):
    """Загрузить конфигурацию из JSON-файла."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Config file not found: {file_path}"
        )
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError as err:
        raise ValueError(f"Invalid JSON: {err}") from err


def validate_field_type(name, value, expected_type):
    """Проверить тип одного поля конфигурации."""
    if not isinstance(value, expected_type):
        raise TypeError(
            f"Field '{name}' must be {expected_type.__name__}."
        )


def validate_non_empty(name, value):
    """Проверить, что строковое поле не пустое."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(
            f"Field '{name}' must be a non-empty string."
        )


def validate_image_extension(name, value):
    """Проверить расширение файла изображения графа."""
    ext = os.path.splitext(value)[1].lower()
    if ext not in IMAGE_EXTENSIONS:
        raise ValueError(
            f"Field '{name}' has unsupported extension: {ext}"
        )


def validate_config(config):
    """Проверить наличие, типы и значения всех параметров."""
    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in config:
            raise KeyError(f"Missing field: '{field}'")
        validate_field_type(field, config[field], expected_type)
    for field in NON_EMPTY_STRING_FIELDS:
        validate_non_empty(field, config[field])
    validate_image_extension(
        "output_image_name", config["output_image_name"]
    )
    return config


def print_config(config):
    """Вывести все параметры в формате ключ-значение."""
    print("--- Configuration ---")
    for key, value in config.items():
        print(f"{key}: {value}")
    print("---------------------")
