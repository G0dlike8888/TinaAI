@echo off
rem ===========================================================
rem  AI Investigation Note Quality Assistant - one-click start.
rem
rem  Double-click this file to run everything.
rem
rem  This file is deliberately plain ASCII: cmd.exe does not read
rem  UTF-8, and non-ASCII characters here corrupt the parsing of
rem  the whole script. All user-facing text lives in the
rem  PowerShell script below, which handles Unicode correctly.
rem ===========================================================
cd /d "%~dp0"
title AI Investigation Note Quality Assistant

if not exist "tools\launcher.ps1" (
    echo.
    echo  [!] Missing: tools\launcher.ps1
    echo      Keep this file in the main project folder, next to
    echo      the 01 Contract, 02 Skill and 03 Demo folders.
    echo.
    pause
    exit /b 1
)

rem A check-only run must never block waiting for a keypress.
set "NOPAUSE="
echo %* | findstr /i /c:"-CheckOnly" >nul 2>&1
if not errorlevel 1 set "NOPAUSE=1"

powershell -NoProfile -ExecutionPolicy Bypass -File "tools\launcher.ps1" %*
set "RC=%ERRORLEVEL%"

if not "%RC%"=="0" (
    echo.
    echo  Launcher finished with code %RC%.
    echo  See START-HERE-BG.md or START-HERE-EN.md for manual steps.
    if not defined NOPAUSE pause
)
exit /b %RC%
