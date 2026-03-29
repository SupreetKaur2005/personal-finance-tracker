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

:: ── PORT CHECKS ─────────────────────────────────────────────────────────────
setlocal enabledelayedexpansion
echo Checking ports...

:: --- Port 8000 (Backend - MUST be free) ---
set BACKEND_PID=
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000 " ^| findstr "LISTENING" 2^>nul') do set BACKEND_PID=%%a
if defined BACKEND_PID (
    echo.
    echo ⚠️  Port 8000 is busy ^(PID !BACKEND_PID!^).
    echo    The backend CANNOT start if port 8000 is occupied.
    set /p KILL_BACKEND=   Kill it and continue? [Y/N]: 
    if /i "!KILL_BACKEND!"=="Y" (
        taskkill /PID !BACKEND_PID! /F >nul 2>&1
        echo    ✅ Port 8000 freed.
    ) else (
        echo    ❌ Aborted. Free port 8000 manually then re-run.
        pause
        exit /b 1
    )
) else (
    echo    ✅ Port 8000 is free.
)

:: --- Port 3001 (Frontend - React will auto-bump if busy) ---
set FRONTEND_PID=
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":3001 " ^| findstr "LISTENING" 2^>nul') do set FRONTEND_PID=%%a
if defined FRONTEND_PID (
    echo    ⚠️  Port 3001 busy ^(PID !FRONTEND_PID!^). React will auto-use next free port.
    echo       CORS accepts any localhost port — app will still work fine.
) else (
    echo    ✅ Port 3001 is free.
)

echo.
:: ── START SERVICES ──────────────────────────────────────────────────────────

:: Start backend
echo Starting Backend ^(FastAPI^) on port 8000...
echo.
start "Finance Tracker - Backend" cmd /k "cd backend && env\Scripts\activate.bat && uvicorn app.main:app --reload --port 8000"

:: Wait for backend to start
echo Waiting for backend to initialize...
timeout /t 5 /nobreak

:: Generate SDK (skip if openapi-generator-cli not found)
echo.
echo Generating Python SDK from OpenAPI...
cd scripts
call ..\backend\env\Scripts\activate.bat 2>nul
python generate_sdk.py
cd ..

:: Start frontend
echo.
echo Starting Frontend ^(React^) on port 3001...
echo.
start "Finance Tracker - Frontend" cmd /k "cd frontend && set PORT=3001 && npm start"

echo.
echo ========================================
echo  ✅ Application started!
echo ========================================
echo.
echo 🌐 Frontend: http://localhost:3001  ^(or next free port if 3001 was busy^)
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo CORS accepts any localhost port — frontend works regardless of which port React picks.
echo Press Ctrl+C in any window to stop the service.
echo.
pause
