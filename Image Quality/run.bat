@echo off
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Starting PyIQA Toolbox...
python run_pyiqa.py

echo Deactivating virtual environment...
deactivate
