@echo off
setlocal EnableDelayedExpansion
chcp 65001 >nul 2>&1

rem Convert all PNG files in the "input" folder to WebP.
rem Outputs go to the "converted" folder. Original PNGs are not deleted.

set "HERE=%~dp0"
if "%HERE:~-1%"=="\" set "HERE=%HERE:~0,-1%"

set "CWEBP=%HERE%\tools\bin\cwebp.exe"
set "INDIR=%HERE%\input"
set "OUTDIR=%HERE%\converted"

rem --- Target size mode (default, good for ~50-100 KB per file) ---
rem Approximate target per image in KB (cwebp -size). Examples:
rem   set WEBP_TARGET_KB=55   (smaller, more detail loss)
rem   set WEBP_TARGET_KB=75   (default)
rem   set WEBP_TARGET_KB=95   (larger, usually cleaner)
if not defined WEBP_TARGET_KB set "WEBP_TARGET_KB=75"

rem --- Fixed quality mode: set WEBP_USE_QUALITY=1 to use constant -q ---
if not defined WEBP_QUALITY set "WEBP_QUALITY=78"

if not exist "%CWEBP%" (
    echo.
    echo [ERROR] cwebp not found:
    echo         %CWEBP%
    echo.
    echo Fix: download the official package:
    echo   https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-1.6.0-windows-x64.zip
    echo Copy bin\cwebp.exe from the ZIP to:
    echo   tools\bin\cwebp.exe
    echo.
    pause
    exit /b 1
)

if not exist "%INDIR%" mkdir "%INDIR%" >nul 2>&1
if not exist "%OUTDIR%" mkdir "%OUTDIR%" >nul 2>&1

set "COUNT=0"
set "FAIL=0"
for %%F in ("%INDIR%\*.png") do (
    if /i not "%%~nxF"=="*.png" set /a COUNT+=1
)

if !COUNT! equ 0 (
    echo No PNG files in: %INDIR%
    echo Put your .png files in the "input" folder, then run this script again.
    pause
    exit /b 0
)

set /a SIZE_BYTES=!WEBP_TARGET_KB!*1024

echo.
if /i "!WEBP_USE_QUALITY!"=="1" (
    echo PNG -^> WebP  (fixed quality -q !WEBP_QUALITY!, method -m 6^)
) else (
    echo PNG -^> WebP  (target ~!WEBP_TARGET_KB! KB per file, method -m 6^)
)
echo Source: %INDIR%
echo Output: %OUTDIR%
echo.

for %%F in ("%INDIR%\*.png") do (
    if /i not "%%~nxF"=="*.png" (
        set "SRC=%%~fF"
        set "BASE=%%~nF"
        set "DST=!OUTDIR!\!BASE!.webp"

        echo Converting: %%~nxF
        if /i "!WEBP_USE_QUALITY!"=="1" (
            "%CWEBP%" -q !WEBP_QUALITY! -m 6 -mt -sharp_yuv -alpha_q 100 -metadata none "!SRC!" -o "!DST!"
        ) else (
            "%CWEBP%" -size !SIZE_BYTES! -m 6 -mt -sharp_yuv -alpha_q 100 -metadata none "!SRC!" -o "!DST!"
        )
        if errorlevel 1 (
            echo   [ERROR] %%~nxF
            set /a FAIL+=1
        ) else (
            for %%A in ("!SRC!") do set "SZ_IN=%%~zA"
            for %%B in ("!DST!") do set "SZ_OUT=%%~zB"
            echo   OK: %%~nxF  ^(!SZ_IN! bytes -^> !SZ_OUT! bytes^)
        )
    )
)

echo.
if !FAIL! gtr 0 (
    echo Done. Failed: !FAIL!
    pause
    exit /b 1
) else (
    echo Done. All WebP files are in the "converted" folder.
    pause
    exit /b 0
)
