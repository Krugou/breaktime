@echo off
REM Enhanced Break Reminder Launch Script
cd /d "%~dp0"

echo ===============================================
echo   Break Reminder - Enhanced Edition
echo ===============================================
echo.
echo Features:
echo  * Modern dark/light themes
echo  * System tray integration
echo  * Configurable settings
echo  * Smooth animations
echo  * Draggable interface
echo.
echo Starting Break Reminder...
echo.

python break_reminder_enhanced.py
echo enhanced version launched
REM If Python execution fails, try the legacy version

if %errorlevel% neq 0 (
    echo.
    echo Enhanced version failed, trying legacy version...
    python break_reminder.py
)
