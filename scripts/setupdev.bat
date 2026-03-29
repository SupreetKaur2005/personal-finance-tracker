@echo off
echo ========================================
echo  Personal Finance Tracker - Setup
echo ========================================
echo.

:: Backend setup
echo [1/5] Setting up backend environment...
cd backend
python -m venv env
call env\Scripts\activate.bat

echo [2/5] Installing backend dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo [3/5] Creating database...
cmd /c "alembic upgrade head"
python -c "import sqlite3; c=sqlite3.connect('finance.db'); c.executescript(open('seed_data.sql').read()); c.close()"

cd ..

:: Frontend setup
echo [4/5] Installing frontend dependencies...
cd frontend
call npm install
call npm audit fix
cd ..

echo [5/5] Installing openapi-generator...
call npm install -g @openapitools/openapi-generator-cli

echo.
echo ========================================
echo  ✅ Setup complete!
echo ========================================
echo.
echo Next steps:
echo 1. Run 'runapplication.bat' to start the application
echo 2. Frontend will open at http://localhost:3000
echo 3. API docs at http://localhost:8000/docs
echo.
pause
