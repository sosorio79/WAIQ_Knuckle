@echo off
REM WAIQ Knuckle - Local launcher (Windows). Default port: 5000
cd /d "%~dp0"

if not exist "venv\Scripts\activate.bat" (
    echo Creating venv...
    python -m venv venv
)
call venv\Scripts\activate.bat

pip install -q -r requirements.txt
python run_web.py
