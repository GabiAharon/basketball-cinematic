@echo off
REM Daily NBA Stats Updater for Basketball Cinematic Showcase
REM This script is designed to be run by Windows Task Scheduler

cd /d "C:\Users\gabia\Desktop\Claude Code\basketball-cinematic"

echo [%date% %time%] Starting stats update... >> update_log.txt
python fetch_stats.py >> update_log.txt 2>&1

if %ERRORLEVEL% EQU 0 (
    echo [%date% %time%] Stats updated successfully. >> update_log.txt
) else (
    echo [%date% %time%] ERROR: Stats update failed with code %ERRORLEVEL%. >> update_log.txt
)
