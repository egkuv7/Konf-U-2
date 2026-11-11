"""Основной исполнительный модуль для этапа 1."""
from src.config import load_config, validate_config, print_config
from src.config import CONFIG_FILE


def run_application():
    """Загрузить, проверить и отобразить конфигурацию."""
    config = load_config(CONFIG_FILE)
    validate_config(config)
    print_config(config)


def handle_config_error(err):
    """Обработка ошибок, связанных с конфигурацией."""
    print(f"[Configuration Error] {err}")


def main():
    """Основная точка входа с обработкой ошибок."""
    try:
        run_application()
    except (
        FileNotFoundError,
        ValueError,
        TypeError,
        KeyError,
    ) as err:
        handle_config_error(err)


if __name__ == "__main__":
    main()
