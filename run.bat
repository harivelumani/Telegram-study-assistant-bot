@echo off
echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error during installation.
    pause
    exit /b %errorlevel%
)

echo Starting the Telegram Bot...
python bot.py
pause
