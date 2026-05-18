@echo off
echo Starting InnerTube API...
echo ----------------------------------------
echo Installing dependencies...
pip install -r requirements.txt
echo ----------------------------------------
echo Starting server...
echo Access the API at http://localhost:8000
echo Documentation at http://localhost:8000/docs
echo ----------------------------------------
python main.py
pause
