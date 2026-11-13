@echo off
cd /d "%~dp0.."
for %%P in (is-number is-odd is-even) do (
    echo ===== %%P =====
    python src\main.py --stage 5 --package %%P --repo https://registry.npmjs.org --ascii-tree --show-order --no-open
)
pause
