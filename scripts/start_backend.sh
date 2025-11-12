#!/bin/bash
# Startup script for backend server

cd backend
python -m venv venv 2>/dev/null || true
source venv/bin/activate
pip install -r requirements.txt --quiet
python main.py

