#!/bin/bash
echo "========================================"
echo " Personal Finance Tracker - Running (Mac/Linux)"
echo "========================================"
echo ""

# Check if backend env exists
if [ ! -d "backend/env" ]; then
    echo "❌ Backend environment not found. Run ./scripts/setupdev.sh first."
    exit 1
fi

# Start backend
echo "Starting Backend (FastAPI) on port 8000..."
(cd backend && source env/bin/activate && uvicorn app.main:app --reload --port 8000) &
BACKEND_PID=$!

# Wait for backend to start
echo "Waiting for backend to initialize..."
sleep 5

# Generate SDK
echo ""
echo "Generating Python SDK from OpenAPI..."
(cd scripts && source ../backend/env/bin/activate 2>/dev/null && python3 generate_sdk.py || echo "Warning: SDK Generator failed.")

# Start frontend
echo ""
echo "Starting Frontend (React) on port 3000..."
(cd frontend && npm start) &
FRONTEND_PID=$!

echo ""
echo "========================================"
echo " ✅ Application started!"
echo "========================================"
echo ""
echo "🌐 Frontend: http://localhost:3000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services."

# Trap Ctrl+C (SIGINT) and kill both child processes
trap "kill $BACKEND_PID $FRONTEND_PID; exit" SIGINT

wait $BACKEND_PID $FRONTEND_PID
