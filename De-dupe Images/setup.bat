@echo off
SETLOCAL

:: Set the project directory to the current directory
set PROJECT_DIR=%~dp0
set VENV_NAME=imagededup_env

echo Creating virtual environment '%VENV_NAME%' with Python 3.11...
py -3.11 -m venv %PROJECT_DIR%%VENV_NAME%

:: Activate virtual environment
call %PROJECT_DIR%%VENV_NAME%\Scripts\activate.bat

echo Installing required packages...
python -m pip install --upgrade pip
pip install imagededup

echo Setup complete! You can now use run.bat to execute the program.
echo.
echo Press any key to exit...
pause >nul

:: Deactivate virtual environment
deactivate

ENDLOCAL
