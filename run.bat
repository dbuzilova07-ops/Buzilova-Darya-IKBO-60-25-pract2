@echo off
cd /d "%~dp0"
python src\main.py --stage 5 --package A --repo tests\fixtures\simple.json --test-mode --ascii-tree --show-order
pause
