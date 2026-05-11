@echo off
cd /d %~dp0
python -m pip install --upgrade pip
python -m pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed --name "WarsztatManager" main.py
pause
