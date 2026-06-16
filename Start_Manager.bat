@echo off
setlocal
cd /d "%~dp0"

if exist ".venv\Scripts\pythonw.exe" (
    start "" ".venv\Scripts\pythonw.exe" "%~dp0main.py"
    exit /b 0
)

where pythonw.exe >nul 2>nul
if %errorlevel%==0 (
    start "" pythonw.exe "%~dp0main.py"
    exit /b 0
)

where pyw.exe >nul 2>nul
if %errorlevel%==0 (
    start "" pyw.exe -3 "%~dp0main.py"
    exit /b 0
)

where python.exe >nul 2>nul
if %errorlevel%==0 (
    start "" python.exe "%~dp0main.py"
    exit /b 0
)

echo Nie znaleziono Python / pythonw / pyw.
echo Zainstaluj Python albo uruchom aplikacje komenda: python main.py
pause
