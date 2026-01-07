@echo off
echo ========================================
echo Windows All-in-One Optimizer
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo Checking dependencies...
python -m pip install -r requirements.txt >nul 2>&1

echo Starting Windows Optimizer...
echo.
echo TIP: Run as Administrator for full functionality!
echo.

REM Run the application
python windows_optimizer.py

if errorlevel 1 (
    echo.
    echo ERROR: Application crashed
    pause
)