@echo off
echo Starting AI Public Speaking Coach...
echo.

echo Setting up media files...
python setup_media.py

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting Flask server...
cd backend
python app.py

pause