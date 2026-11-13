"""Validate test repository JSON with uppercase package names."""

import json
from pathlib import Path
import re

TEST_NAME = re.compile(r"^[A-Z]+$")

def load_fixture(path):
    """Load graph from JSON mapping of uppercase package names to lists."""
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(
            f"Не удалось прочитать тестовый граф: {error}"
        ) from error
    if not isinstance(data, dict) or not data:
        raise ValueError("Тестовый граф должен быть непустым JSON-объектом")
    if any(not TEST_NAME.fullmatch(name) for name in data):
        raise ValueError("Имена вершин должны содержать только A-Z")
    for name, dependencies in data.items():
        if not isinstance(dependencies, list):
            raise ValueError(
                f"У вершины {name} должен быть список зависимостей"
            )
        if any(not isinstance(dep, str) or dep not in data
               for dep in dependencies):
            raise ValueError(f"У вершины {name} есть неизвестная зависимость")
    return {name: sorted(set(deps)) for name, deps in data.items()}


