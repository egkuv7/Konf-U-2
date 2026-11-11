"""Парсер индекса Packages менеджера пакетов Ubuntu (apt)."""
import gzip
import lzma
import urllib.request

TIMEOUT_SECONDS = 30
USER_AGENT = "dep-graph-tool/2.0"
GZ_SUFFIX = ".gz"
XZ_SUFFIX = ".xz"
PACKAGE_FIELD = "Package"
VERSION_FIELD = "Version"
DEPENDS_FIELD = "Depends"


def fetch_index(repo_url, test_mode):
    """Загрузить индекс Packages по URL или из локального файла."""
    if test_mode:
        with open(repo_url, "r", encoding="utf-8") as file:
            return file.read()
    request = urllib.request.Request(
        repo_url, headers={"User-Agent": USER_AGENT}
    )
    with urllib.request.urlopen(
        request, timeout=TIMEOUT_SECONDS
    ) as response:
        data = response.read()
    if repo_url.endswith(GZ_SUFFIX):
        return gzip.decompress(data).decode("utf-8")
    if repo_url.endswith(XZ_SUFFIX):
        return lzma.decompress(data).decode("utf-8")
    return data.decode("utf-8")


def parse_fields(stanza):
    """Разобрать одну запись Packages в словарь полей."""
    fields = {}
    key = None
    for line in stanza.split("\n"):
        if not line.strip():
            continue
        if line[0] in " \t" and key:
            fields[key] += " " + line.strip()
        elif ": " in line:
            key, value = line.split(": ", 1)
            fields[key] = value.strip()
    return fields


def find_package(text, name, version):
    """Найти запись пакета с точным совпадением имени и версии."""
    for stanza in text.split("\n\n"):
        fields = parse_fields(stanza)
        if fields.get(PACKAGE_FIELD) != name:
            continue
        if fields.get(VERSION_FIELD) == version:
            return fields
    return None


def clean_name(dependency):
    """Убрать из имени зависимости версию и суффикс архитектуры."""
    name = dependency.split("(")[0]
    name = name.split(":")[0]
    return name.strip()


def parse_depends(depends):
    """Разобрать поле Depends на список прямых зависимостей."""
    result = []
    for group in depends.split(","):
        names = [clean_name(alt) for alt in group.split("|")]
        names = [n for n in names if n and not n.startswith("$")]
        if names:
            result.append(" | ".join(names))
    return result


def print_dependencies(name, version, deps):
    """Вывести на экран все прямые зависимости пакета."""
    print(f"--- Direct dependencies of {name} ({version}) ---")
    if not deps:
        print("No dependencies found.")
    for dep in deps:
        print(f"- {dep}")
    print("----------------------------------------")
