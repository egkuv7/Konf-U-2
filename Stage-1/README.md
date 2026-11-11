# Инструмент визуализации графа зависимостей для менеджера пакетов — Этап 1

## 1. Общее описание

Минимальный прототип CLI-приложения для визуализации графа зависимостей
менеджера пакетов Ubuntu (apt). На данном этапе реализована только работа
с конфигурацией: чтение параметров из JSON-файла, их строгая валидация
и вывод в консоль в формате ключ-значение.

Логика сбора зависимостей, построения графа и визуализации будет добавлена
на последующих этапах разработки.

**Цель этапа:** создать минимальное CLI-приложение и сделать его
настраиваемым через внешний конфигурационный файл.

**Язык реализации:** Python 3.

**Формат конфигурации:** JSON.

## 2. Описание функций и настроек

### 2.1. Настраиваемые параметры (config.json)

| Параметр              | Тип    | Описание                                                   |
|-----------------------|--------|------------------------------------------------------------|
| `package_name`        | `str`  | Имя анализируемого пакета                                  |
| `repo_url`            | `str`  | URL-адрес репозитория или путь к файлу тестового репозитория |
| `test_mode`           | `bool` | Режим работы с тестовым репозиторием                       |
| `package_version`     | `str`  | Версия анализируемого пакета                               |
| `output_image_name`   | `str`  | Имя сгенерированного файла с изображением графа            |
| `ascii_tree_mode`     | `bool` | Режим вывода зависимостей в формате ASCII-дерева           |
| `filter_substring`    | `str`  | Подстрока для фильтрации пакетов                           |

### 2.2. Основные функции

#### Модуль `src/config.py`

- **`load_config(file_path)`** — загрузка JSON-файла конфигурации.
  Проверяет существование файла и корректность синтаксиса.
  Бросает `FileNotFoundError` или `ValueError` при ошибках.

- **`validate_field_type(name, value, expected_type)`** — проверка
  соответствия типа отдельного поля ожидаемому типу.
  Бросает `TypeError` при несовпадении.

- **`validate_non_empty(name, value)`** — проверка, что строковое
  поле не является пустым. Бросает `ValueError`.

- **`validate_image_extension(name, value)`** — проверка корректности
  расширения файла изображения (поддерживаются `.png`, `.svg`,
  `.jpg`, `.jpeg`). Бросает `ValueError`.

- **`validate_config(config)`** — оркестрация всех проверок:
  наличие полей, типы, непустота строк, расширение изображения.

- **`print_config(config)`** — вывод всех параметров в формате
  ключ-значение.

#### Модуль `src/main.py`

- **`run_application()`** — загрузка, валидация и вывод конфигурации.

- **`handle_config_error(err)`** — централизованная обработка ошибок
  конфигурации.

- **`main()`** — точка входа приложения с обработкой всех возможных
  исключений (`FileNotFoundError`, `ValueError`, `TypeError`,
  `KeyError`).

## 3. Команды для сборки проекта и запуска тестов

Проект написан на интерпретируемом языке Python и не требует сборки.
Достаточно установить Python 3.8 или выше.

### Запуск через скрипт (Linux/macOS)

```bash
chmod +x run.sh
./run.sh
```

Скрипт `run.sh` последовательно выполняет:
1. Запуск всех модульных тестов.
2. Запуск основного приложения.

### Запуск через скрипт (Windows)

```cmd
run.bat
```

Скрипт `run.bat` выполняет те же действия, что и `run.sh`.

### Ручной запуск тестов

**Linux/macOS:**
```bash
python3 -m unittest discover -s tests
```

**Windows:**
```cmd
py -u -m unittest discover -s tests
```

### Ручной запуск приложения

**Linux/macOS:**
```bash
python3 -m src.main
```

**Windows:**
```cmd
py -u -m src.main
```

### Проверка качества кода

**Linux/macOS:**
```bash
python3 -m pylint src/
python3 -m flake8 src/
```

**Windows:**
```cmd
python -m pylint src/
python -m flake8 src/
```

## 4. Примеры использования

### 4.1. Успешный запуск

**Файл `config.json`:**

```json
{
    "package_name": "curl",
    "repo_url": "http://archive.ubuntu.com/ubuntu/dists/jammy/main/binary-amd64/Packages.gz",
    "test_mode": true,
    "package_version": "7.81.0-1",
    "output_image_name": "graph.png",
    "ascii_tree_mode": false,
    "filter_substring": "lib"
}
```

**Вывод в консоль:**

```text
--- Configuration ---
package_name: curl
repo_url: http://archive.ubuntu.com/ubuntu/dists/jammy/main/binary-amd64/Packages.gz
test_mode: True
package_version: 7.81.0-1
output_image_name: graph.png
ascii_tree_mode: False
filter_substring: lib
---------------------
```

### 4.2. Обработка ошибок

#### Отсутствующий файл конфигурации

```text
[Configuration Error] Config file not found: config.json
```

#### Некорректный JSON-синтаксис

```text
[Configuration Error] Invalid JSON: Expecting ',' delimiter: line 3 column 5 (char 42)
```

#### Отсутствующее обязательное поле

```text
[Configuration Error] Missing field: 'package_version'
```

#### Неверный тип поля

```text
[Configuration Error] Field 'test_mode' must be bool.
```

#### Пустая строка в обязательном поле

```text
[Configuration Error] Field 'package_name' must be a non-empty string.
```

#### Неподдерживаемое расширение изображения

```text
[Configuration Error] Field 'output_image_name' has unsupported extension: .bmp
```

### 4.3. Запуск тестов

**Linux/macOS:**
```text
$ python3 -m unittest discover -s tests
........
----------------------------------------------------------------------
Ran 7 tests in 0.022s

OK
```

**Windows:**
```cmd
C:\project> py -u -m unittest discover -s tests
.......
----------------------------------------------------------------------
Ran 7 tests in 0.022s

OK
```
--------
2026
