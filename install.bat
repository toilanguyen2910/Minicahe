@REM Minicahe installer for Windows
@REM Usage: install.bat
echo off

setlocal

echo.
echo === Minicahe Installer ^<3^> ===
echo.

echo Looking for Python...
where python >nul 2>&1
if errorlevel 1 (
    echo Python not found. Please install Python 3.9+ from https://python.org
    pause
    exit /b 1
)

echo Found Python:
python --version

echo.
echo Installing Minicahe...
pip install --upgrade pip -q
pip install minicahe -q 2>nul || (
    echo Installing from source...
    pip install -e .
)

echo.
echo Minicahe installed successfully!
echo.
echo Try: minicahe compress --help
echo.
pause
