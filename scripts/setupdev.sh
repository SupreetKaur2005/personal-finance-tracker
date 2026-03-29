#!/bin/bash
echo "========================================"
echo " Personal Finance Tracker - Setup (Mac/Linux)"
echo "========================================"
echo ""

# Backend setup
echo "[1/4] Setting up backend environment..."
cd backend || exit
python3 -m venv env
source env/bin/activate

echo "[2/4] Installing backend dependencies..."
python3 -m pip install --upgrade pip
pip install -r requirements.txt

echo "[3/4] Creating database..."
alembic upgrade head
python3 -c "import sqlite3; c=sqlite3.connect('finance.db'); c.executescript(open('seed_data.sql').read()); c.close()"

cd .. || exit

# Frontend setup
echo "[4/4] Installing frontend dependencies..."
cd frontend || exit
npm install
cd .. || exit

echo ""
echo "========================================"
echo " ✅ Setup complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "Run './scripts/runapplication.sh' to start the application"
