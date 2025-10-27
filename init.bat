@echo off
REM CADE System Initialization Script for Windows

echo [*] Starting CADE System Initialization...

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Run the initialization script
echo [*] Running initialization script...
python init_cade.py

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Initialization failed. Check the output above for details.
    pause
    exit /b 1
)

echo [*] Initialization completed successfully!
echo.
echo To activate the virtual environment, run:
echo    .\\venv\\Scripts\\activate

echo.
echo To start the CADE system, run:
echo    .\\venv\\Scripts\\python -m cade_production

pause
