@echo off
title ComicCraft AI Studio Launcher
echo ========================================================
echo   Launching ComicCraft AI Studio...
echo ========================================================
echo.

cd /d "%~dp0"

IF EXIST ".venv\Scripts\python.exe" (
    echo Using Virtual Environment (.venv)...
    start http://127.0.0.1:8000
    ".venv\Scripts\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
) ELSE (
    echo Using System Python...
    start http://127.0.0.1:8000
    python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
)

pause
