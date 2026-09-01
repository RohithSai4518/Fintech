@echo off
REM =========================================================================
REM  Fintech Enterprise Platform Launch Script (Windows)
REM =========================================================================

echo [1/2] Running automated test suite...
python -m unittest discover -s tests -v
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Unit tests failed. Aborting server launch.
    exit /b %ERRORLEVEL%
)

echo.
echo [2/2] Launching Fintech Core Banking & Trading Platform...
python backend\server\app.py
