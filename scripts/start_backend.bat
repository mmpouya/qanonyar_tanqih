@echo off
REM Startup script for backend server (Windows)

cd backend
python -m venv venv 2>nul
call venv\Scripts\activate.bat
pip install -r requirements.txt --quiet
python main.py

