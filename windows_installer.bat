@echo off
title June Bot Installer
color 0B

echo ==========================================
echo          June Bot Installer
echo ==========================================
echo.

:: -------------------------------------------------
:: Python
:: -------------------------------------------------

python --version >nul 2>&1

if errorlevel 1 (
    color 0C
    echo Python is not installed.
    echo.
    echo Download Python:
    echo https://www.python.org/downloads/
    pause
    exit /b
)

echo [OK] Python detected.

:: -------------------------------------------------
:: Project structure
:: -------------------------------------------------

echo.
echo Checking project...

set FILES=^
app\main.py ^
app\poems.py ^
app\styles.py ^
app\daily.py ^
app\challenge.py ^
db\database.py ^
app\explain.py ^
db\db.sql ^
db\init_db.py ^
requirements.txt

for %%f in (%FILES%) do (
    if not exist %%f (
        color 0C
        echo Missing file:
        echo %%f
        pause
        exit /b
    )
)

echo [OK] Project integrity verified.

:: -------------------------------------------------
:: Virtual environment
:: -------------------------------------------------

if not exist ".venv" (
    echo.
    echo Creating virtual environment...
    python -m venv .venv
)

call .venv\Scripts\activate

:: -------------------------------------------------
:: Pip
:: -------------------------------------------------

python -m pip install --upgrade pip

pip install -r requirements.txt

:: -------------------------------------------------
:: .env
:: -------------------------------------------------

if not exist ".env" (

echo Creating .env

(
echo DISCORD_TOKEN=
echo OPENROUTER_API_KEY=
)> .env

)

:: -------------------------------------------------
:: Database
:: -------------------------------------------------

python db\init_db.py

echo.

echo.
echo ==========================================
echo Installation completed successfully!
echo ==========================================
echo.
echo Don't forget to fill your .env file:
echo.
echo DISCORD_TOKEN=YOUR_DISCORD_TOKEN
echo OPENROUTER_API_KEY=YOUR_OPENROUTER_API_KEY
echo.

choice /C YN /M "Launch June Bot now?"

if errorlevel 2 (
    echo.
    echo You can launch the bot later with launcher.bat
    pause
    exit /b
)

call windows_launcher.bat