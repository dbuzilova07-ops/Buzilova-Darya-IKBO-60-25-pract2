@echo off
cd /d "%~dp0"
python src\main.py --stage 4 --package A --repo tests\fixtures\simple.json --test-mode --show-order
pause
