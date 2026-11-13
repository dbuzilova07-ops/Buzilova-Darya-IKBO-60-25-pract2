@echo off
cd /d "%~dp0.."
python -m unittest discover -s tests -p "test_*.py" -v
if errorlevel 1 exit /b 1
python src\main.py --stage 3 --package A --repo tests\fixtures\cycle.json --test-mode
python src\main.py --stage 5 --package A --repo tests\fixtures\deep.json --test-mode --ascii-tree --show-order --no-open
pause
