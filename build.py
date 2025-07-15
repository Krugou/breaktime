"""Build script for creating executable files."""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_exe():
    """Build executable using PyInstaller."""
    
    # Define paths
    script_dir = Path(__file__).parent
    main_script = script_dir / "break_reminder_enhanced.py"
    build_dir = script_dir / "build"
    dist_dir = script_dir / "dist"
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",  # No console window
        "--name=BreakReminder",
        "--add-data", f"{script_dir / 'src'};src",
        "--hidden-import", "PyQt5.QtCore",
        "--hidden-import", "PyQt5.QtGui", 
        "--hidden-import", "PyQt5.QtWidgets",
        "--distpath", str(dist_dir),
        "--workpath", str(build_dir),
        "--specpath", str(script_dir),
        str(main_script)
    ]
    
    print("Building executable...")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True)
        print("\\nBuild completed successfully!")
        print(f"Executable created at: {dist_dir / 'BreakReminder.exe'}")
        
        # Create a simple installer bat file
        create_installer_bat()
        
    except subprocess.CalledProcessError as e:
        print(f"\\nBuild failed with error: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("\\nError: PyInstaller not found. Please install it with: pip install pyinstaller")
        sys.exit(1)

def create_installer_bat():
    """Create a simple installer batch file."""
    
    script_dir = Path(__file__).parent
    bat_content = '''@echo off
echo Break Reminder - Enhanced Edition
echo ================================
echo.
echo This will install Break Reminder to your system.
echo.
pause

REM Create installation directory
set INSTALL_DIR=%USERPROFILE%\\AppData\\Local\\BreakReminder
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copy executable
copy "dist\\BreakReminder.exe" "%INSTALL_DIR%\\BreakReminder.exe"

REM Create desktop shortcut
set DESKTOP=%USERPROFILE%\\Desktop
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\\shortcut.vbs"
echo sLinkFile = "%DESKTOP%\\Break Reminder.lnk" >> "%TEMP%\\shortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\\shortcut.vbs"
echo oLink.TargetPath = "%INSTALL_DIR%\\BreakReminder.exe" >> "%TEMP%\\shortcut.vbs"
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> "%TEMP%\\shortcut.vbs"
echo oLink.Description = "Break Reminder - Enhanced Edition" >> "%TEMP%\\shortcut.vbs"
echo oLink.Save >> "%TEMP%\\shortcut.vbs"
cscript /nologo "%TEMP%\\shortcut.vbs"
del "%TEMP%\\shortcut.vbs"

REM Create start menu shortcut
set STARTMENU=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\\shortcut.vbs"
echo sLinkFile = "%STARTMENU%\\Break Reminder.lnk" >> "%TEMP%\\shortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\\shortcut.vbs"
echo oLink.TargetPath = "%INSTALL_DIR%\\BreakReminder.exe" >> "%TEMP%\\shortcut.vbs"
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> "%TEMP%\\shortcut.vbs"
echo oLink.Description = "Break Reminder - Enhanced Edition" >> "%TEMP%\\shortcut.vbs"
echo oLink.Save >> "%TEMP%\\shortcut.vbs"
cscript /nologo "%TEMP%\\shortcut.vbs"
del "%TEMP%\\shortcut.vbs"

echo.
echo Installation completed!
echo.
echo Desktop shortcut created: %DESKTOP%\\Break Reminder.lnk
echo Start menu shortcut created: %STARTMENU%\\Break Reminder.lnk
echo.
echo You can now run Break Reminder from your desktop or start menu.
echo.
pause
'''
    
    installer_path = script_dir / "install.bat"
    with open(installer_path, 'w') as f:
        f.write(bat_content)
    
    print(f"Installer created at: {installer_path}")

if __name__ == "__main__":
    build_exe()