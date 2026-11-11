"""Точка входа приложения: этап 2, сбор данных о зависимостях."""
import urllib.error

from src.config import CONFIG_FILE, load_config, print_config
from src.config import validate_config
from src.apt_parser import fetch_index, find_package, parse_depends
from src.apt_parser import print_dependencies


def collect_dependencies(config):
    """Получить прямые зависимости пакета заданной версии."""
    text = fetch_index(config["repo_url"], config["test_mode"])
    fields = find_package(
        text, config["package_name"], config["package_version"]
    )
    if fields is None:
        raise LookupError(
            f"Package {config['package_name']} "
            f"version {config['package_version']} not found"
        )
    return parse_depends(fields.get("Depends", ""))


def run_application():
    """Загрузить конфигурацию и вывести прямые зависимости."""
    config = load_config(CONFIG_FILE)
    validate_config(config)
    print_config(config)
    deps = collect_dependencies(config)
    print_dependencies(
        config["package_name"], config["package_version"], deps
    )


def main():
    """Точка входа с обработкой ошибок конфигурации и данных."""
    try:
        run_application()
    except (FileNotFoundError, ValueError, TypeError, KeyError) as err:
        print(f"[Configuration Error] {err}")
    except LookupError as err:
        print(f"[Repository Error] {err}")
    except urllib.error.URLError as err:
        print(f"[Network Error] {err}")
    except OSError as err:
        print(f"[I/O Error] {err}")


if __name__ == "__main__":
    main()
