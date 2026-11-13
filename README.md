# Граф зависимостей npm — вариант 2

## Этапы 1–3

CLI и получение прямых зависимостей через npm Registry. Добавлен поиск
транзитивных зависимостей BFS без рекурсии, защита от циклов и тестовый JSON.

```powershell
python src/main.py --stage 3 --package A --repo tests/fixtures/cycle.json --test-mode
```

Тесты: `python -m unittest discover -s tests -p "test_*.py" -v`.
