@echo off
SETLOCAL EnableDelayedExpansion

:: Set the project directory to the current directory
set PROJECT_DIR=%~dp0
set VENV_NAME=imagededup_env

:: Check if virtual environment exists
if not exist "!PROJECT_DIR!!VENV_NAME!\Scripts\activate.bat" (
    echo Virtual environment not found! Please run setup.bat first.
    pause
    exit /b 1
)

:: Activate virtual environment and handle potential errors
call "!PROJECT_DIR!!VENV_NAME!\Scripts\activate.bat"
if errorlevel 1 (
    echo Failed to activate virtual environment
    pause
    exit /b 1
)

:: Install imagededup if not already installed
"!PROJECT_DIR!!VENV_NAME!\Scripts\python.exe" -m pip install imagededup
if errorlevel 1 (
    echo Failed to install imagededup package
    pause
    exit /b 1
)

:: Prompt user for image directory
set /p IMAGE_DIR="Enter the path to your image directory: "

:: Validate directory exists
if not exist "!IMAGE_DIR!" (
    echo Error: Directory does not exist!
    pause
    exit /b 1
)

:: Run the Python script using the Python from virtual environment
"!PROJECT_DIR!!VENV_NAME!\Scripts\python.exe" "!PROJECT_DIR!imagededup_script.py" "!IMAGE_DIR!"
if errorlevel 1 (
    echo Failed to run the Python script
    pause
    exit /b 1
)

:: Deactivate virtual environment
call deactivate

ENDLOCAL
