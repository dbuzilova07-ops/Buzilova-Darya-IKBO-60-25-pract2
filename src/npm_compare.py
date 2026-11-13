"""Compare declared direct dependencies with npm's native view command."""

import json
import shutil
import subprocess


def compare_direct_with_npm(package, registry, our_dependencies):
    """Run npm view and compare direct dependency names when npm is present."""
    if shutil.which("npm") is None:
        print("npm CLI не найден. Установи Node.js для сравнения с npm.")
        return False
    command = [
        "npm", "view", package, "dependencies", "--json",
        "--registry", registry,
    ]
    try:
        result = subprocess.run(
            command, capture_output=True, text=True, timeout=40,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        print(f"Сравнение с npm не выполнено: {error}")
        return False
    if result.returncode:
        print(f"npm view завершился с ошибкой: {result.stderr.strip()}")
        return False
    try:
        npm_data = json.loads(result.stdout or "{}")
    except json.JSONDecodeError:
        print("npm вернул некорректный JSON")
        return False
    if not isinstance(npm_data, dict):
        print("npm вернул данные в неожиданном формате")
        return False
    ours = set(our_dependencies)
    theirs = set(npm_data)
    print("Сравнение прямых зависимостей с npm view:")
    print("  Совпали:", ", ".join(sorted(ours & theirs)) or "нет")
    print("  Только у нас:", ", ".join(sorted(ours - theirs)) or "нет")
    print("  Только у npm:", ", ".join(sorted(theirs - ours)) or "нет")
    print("npm ls --all показывает установленные пакеты, не время загрузки.")
    return ours == theirs
