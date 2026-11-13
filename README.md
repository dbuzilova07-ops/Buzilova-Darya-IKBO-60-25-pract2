# Граф зависимостей npm — вариант 2

## Этапы 1–2

Python CLI принимает `--package`, `--repo`, `--test-mode`, `--ascii-tree`.
В этапе 1 показывает параметры, в этапе 2 получает прямые зависимости
пакета через HTTP из npm Registry, без npm-библиотек.

```powershell
python src/main.py --stage 2 --package is-odd --repo https://registry.npmjs.org
```

Тестовый режим:

```powershell
python src/main.py --stage 2 --package A --repo tests/fixtures/simple.json --test-mode
```
