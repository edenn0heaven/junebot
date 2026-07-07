@echo off
title June Bot

if not exist ".venv" (
    echo.
    echo June Bot is not installed.
    echo Run windows_installer.bat first.
    pause
    exit /b
)

call .venv\Scripts\activate

python -m app.main

pause