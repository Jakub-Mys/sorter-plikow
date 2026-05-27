@echo off
cd /d "%~dp0"

if exist .venv\Scripts\python.exe (
    echo Uruchamianie przez srodowisko wirtualne...
    .venv\Scripts\python.exe main.py
) else (
    echo Uruchamianie przez globalnego Pythona...
    python main.py
)

echo.
echo Zrobione!
pause