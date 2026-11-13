@echo off
cd /d "%~dp0"
python src\main.py --stage 1 --package A --repo tests\fixtures\simple.json --test-mode
pause
