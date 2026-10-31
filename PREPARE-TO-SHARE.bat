@echo off
rem ===========================================================
rem  Prepare this folder for sharing with someone else.
rem
rem  Double-click this file BEFORE you copy or send the folder.
rem  It removes YOUR personal API key (your billable credential)
rem  and the local .venv environment, so the recipient starts
rem  clean: START-ASSISTANT.bat will rebuild everything on their
rem  machine and ask for THEIR OWN key.
rem
rem  Plain ASCII on purpose - cmd.exe cannot read UTF-8.
rem ===========================================================
cd /d "%~dp0"
title Prepare folder for sharing

if not exist "tools\launcher.ps1" (
    echo.
    echo  [!] Missing: tools\launcher.ps1
    echo      Keep this file in the main project folder, next to
    echo      the 01 Contract, 02 Skill and 03 Demo folders.
    echo.
    pause
    exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -File "tools\launcher.ps1" -PrepareShare
set "RC=%ERRORLEVEL%"

if not "%RC%"=="0" (
    echo.
    echo  Preparation did NOT finish cleanly - code %RC%.
    echo  Read the message above: your API key may still be in the folder.
    echo  Do not share the folder until this succeeds.
    pause
)
exit /b %RC%
