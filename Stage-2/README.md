# Инструмент визуализации графа зависимостей для менеджера пакетов — Этап 2

## 1. Общее описание

Этап 2 «Сбор данных»: приложение получает индекс репозитория Ubuntu (apt),
находит запись пакета с точно заданной версией и выводит на экран все его
прямые зависимости. Информация извлекается разбором файла Packages
собственным парсером — менеджеры пакетов и сторонние библиотеки не
используются, только стандартная библиотека Python (urllib, gzip, lzma).
Конфигурация этапа 1 (JSON, 7 параметров) сохранена. Параметр
filter_substring будет задействован на этапе 3.

## 2. Описание функций и настроек

### Настройки (config.json)
| Параметр | Тип | Описание |
|---|---|---|
| package_name | str | Имя анализируемого пакета |
| repo_url | str | URL индекса Packages (.gz/.xz/текст) или путь к файлу |
| test_mode | bool | Режим работы с тестовым репозиторием |
| package_version | str | Версия пакета (точное совпадение) |
| output_image_name | str | Имя будущего файла изображения графа |
| ascii_tree_mode | bool | Режим ASCII-дерева (этап 5) |
| filter_substring | str | Подстрока фильтрации (этап 3) |

### Модуль src/apt_parser.py
- fetch_index(repo_url, test_mode) — загрузка индекса по URL или из
  локального файла; распаковка .gz и .xz.
- parse_fields(stanza) — разбор записи Packages в словарь полей,
  склейка многострочных полей.
- find_package(text, name, version) — поиск по точному имени и версии.
- clean_name(dependency) — очистка имени от версии и суффикса :any.
- parse_depends(depends) — разбор Depends: группы через запятую,
  альтернативы «a | b» сохраняются одной группой.
- print_dependencies(name, version, deps) — вывод зависимостей.

### Модуль src/main.py
- collect_dependencies(config) — сбор прямых зависимостей.
- run_application() — конфигурация + сбор + вывод.
- main() — обработка ошибок: конфигурации, отсутствия пакета,
  сети и ввода-вывода.

### Модуль src/config.py
Загрузка и валидация JSON (см. этап 1): наличие полей, типы,
непустые строки, расширение изображения.

## 3. Команды для сборки проекта и запуска тестов

Сборка не требуется, нужен Python 3.8+.

Windows (cmd/PowerShell):
```cmd
run.bat
py -u -m unittest discover -s tests
py -u -m src.main
```

Linux/macOS:
```bash
chmod +x run.sh
./run.sh
python3 -m unittest discover -s tests
python3 -m src.main
```

## 4. Примеры использования

### Тестовый режим (по умолчанию)
```text
--- Configuration ---
package_name: curl
repo_url: tests/mock_packages.txt
test_mode: True
package_version: 7.81.0-1ubuntu1.16
output_image_name: graph.svg
ascii_tree_mode: False
filter_substring: lib
---------------------
--- Direct dependencies of curl (7.81.0-1ubuntu1.16) ---
- libc6
- libcurl4
- zlib1g
----------------------------------------
```

### Реальный репозиторий
```json
{
    "package_name": "bash",
    "repo_url": "http://archive.ubuntu.com/ubuntu/dists/jammy/main/binary-amd64/Packages.gz",
    "test_mode": false,
    "package_version": "5.1-6ubuntu1",
    "output_image_name": "graph.svg",
    "ascii_tree_mode": false,
    "filter_substring": ""
}
```
Версия должна точно присутствовать в выбранном индексе; для обновлённых
версий используйте индекс jammy-updates.

### Обработка ошибок
```text
[Repository Error] Package curl version 0.0 not found
[Network Error] <urlopen error [Errno -2] Name or service not known>
[Configuration Error] Field 'test_mode' must be bool.
```

### Запуск тестов
```text
Ran 17 tests in 0.001s

OK
```
----------
2026
