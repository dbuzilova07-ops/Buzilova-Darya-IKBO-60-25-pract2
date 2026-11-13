@echo off
cd /d "%~dp0.."
where npm >nul 2>nul
if errorlevel 1 (
    echo npm CLI ne naiden. Ustanovite Node.js.
    pause
    exit /b 1
)
python src\main.py --stage 4 --package is-even --repo https://registry.npmjs.org --show-order --compare-npm
if errorlevel 1 exit /b 1
rem npm ls shows installed packages, not their temporal download order.
if not exist "output\npm_compare" mkdir "output\npm_compare"
npm install is-even --prefix "output\npm_compare" --ignore-scripts --no-audit --no-fund --no-save
npm ls --prefix "output\npm_compare" --all
pause
