@echo off
setlocal
cd /d "%~dp0" || exit /b 1

where python >nul 2>nul
if errorlevel 1 (
    where py >nul 2>nul
    if errorlevel 1 (
        echo Python is not installed or not on PATH.
        exit /b 1
    )
    set "PYTHON_CMD=py -3"
) else (
    set "PYTHON_CMD=python"
)

if not exist "%~dp0venv\Scripts\python.exe" (
    %PYTHON_CMD% -m venv "%~dp0venv"
    if errorlevel 1 exit /b 1
)

"%~dp0venv\Scripts\python.exe" -m pip install -r "%~dp0requirements.txt"
if errorlevel 1 exit /b 1

"%~dp0venv\Scripts\python.exe" "%~dp0gen_sample_image.py"
if errorlevel 1 exit /b 1

"%~dp0venv\Scripts\python.exe" "%~dp0app.py"
exit /b %errorlevel%
