# Граф зависимостей npm — вариант 2

## Этап 1 — CLI с конфигурацией

Программа на Python принимает параметры `--package`, `--repo`, `--test-mode`,
`--ascii-tree`, проверяет ошибки ввода и показывает значения ключ–значение.

Запуск: `python src/main.py --stage 1 --package A --repo tests/fixtures/simple.json --test-mode`.

Запуск тестов: `python -m unittest discover -s tests -p "test_*.py" -v`
(тесты добавляются постепенно вместе с новыми этапами).
