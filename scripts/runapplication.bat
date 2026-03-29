@echo off
echo ========================================
echo  Personal Finance Tracker - Running
echo ========================================
echo.

:: Check if backend env exists
if not exist "backend\env" (
    echo ❌ Backend environment not found. Run setupdev.bat first.
    pause
    exit /b 1
)

:: Start backend
echo Starting Backend (FastAPI) on port 8000...
echo.
start "Finance Tracker - Backend" cmd /k "cd backend && env\Scripts\activate.bat && uvicorn app.main:app --reload --port 8000"

:: Wait for backend to start
echo Waiting for backend to initialize...
timeout /t 5 /nobreak

:: Generate SDK (skip if openapi-generator-cli not found)
echo.
echo Generating Python SDK from OpenAPI...
cd scripts
call env\Scripts\activate.bat 2>nul
python generate_sdk.py
cd ..

:: Start frontend
echo.
echo Starting Frontend (React) on port 3000...
echo.
start "Finance Tracker - Frontend" cmd /k "cd frontend && npm start"

echo.
echo ========================================
echo  ✅ Application started!
echo ========================================
echo.
echo 🌐 Frontend: http://localhost:3000
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo The application windows will open automatically.
echo Press Ctrl+C in any window to stop the service.
echo.
pause
