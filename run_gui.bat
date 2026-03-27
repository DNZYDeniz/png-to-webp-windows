@echo off
setlocal EnableExtensions
chcp 65001 >nul 2>&1
title png-to-webp-windows (desktop GUI)
cd /d "%~dp0"

if not exist "%~dp0gui\png_to_webp_gui.py" (
    echo [ERROR] gui\png_to_webp_gui.py not found. Run from the pngtowebp folder.
    pause
    exit /b 1
)

set "PATH=%LocalAppData%\Programs\Python\Launcher;%PATH%"
set "PATH=%LocalAppData%\Programs\Python\Python314;%LocalAppData%\Programs\Python\Python313;%LocalAppData%\Programs\Python\Python312;%LocalAppData%\Programs\Python\Python311;%PATH%"
set "PATH=%ProgramFiles%\Python314;%ProgramFiles%\Python313;%ProgramFiles%\Python312;%PATH%"
set "PATH=%LocalAppData%\Microsoft\WindowsApps;%PATH%"

echo Starting desktop GUI (installs customtkinter on first run if needed)...
echo.

where py >nul 2>&1
if %errorlevel% equ 0 (
    py -3 "%~dp0gui\png_to_webp_gui.py"
    goto :after_run
)

where python >nul 2>&1
if %errorlevel% equ 0 (
    python "%~dp0gui\png_to_webp_gui.py"
    goto :after_run
)

where python3 >nul 2>&1
if %errorlevel% equ 0 (
    python3 "%~dp0gui\png_to_webp_gui.py"
    goto :after_run
)

echo.
echo [ERROR] Python not found. Install from https://www.python.org/downloads/
echo Enable "Add python.exe to PATH" in the installer.
echo.
pause
exit /b 1

:after_run
if errorlevel 1 (
    echo.
    echo [ERROR] The program exited with an error.
    echo If pip could not install customtkinter, run: pip install customtkinter
    echo.
    pause
    endlocal
    exit /b 1
)

endlocal
exit /b 0
