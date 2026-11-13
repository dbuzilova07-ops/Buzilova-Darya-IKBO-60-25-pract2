# Граф зависимостей npm — вариант 2

## Этапы 1–4

Консольный анализатор зависимостей npm на Python. Получение прямых
зависимостей и BFS реализованы без менеджеров пакетов и npm-библиотек.
Поддерживается топологический порядок (зависимости перед пакетами) и
сравнение с `npm view` при установленном Node.js.

```powershell
python src/main.py --stage 4 --package A --repo tests/fixtures/simple.json --test-mode --show-order
python src/main.py --stage 4 --package is-even --repo https://registry.npmjs.org --show-order --compare-npm
```

При цикле корректный строгий порядок невозможен, показывается предупреждение.
