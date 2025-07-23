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
    
    # PyInstaller command with improved single-file executable settings
    cmd = [
        "pyinstaller",
        "--onefile",           # Single file executable
        "--windowed",          # No console window
        "--name=BreakReminder",
        "--clean",             # Clean build
        "--noconfirm",         # Overwrite without confirmation
        f"--add-data={script_dir / 'src'}:src",  # Fixed path separator for Linux
        "--hidden-import=PyQt5.QtCore",
        "--hidden-import=PyQt5.QtGui", 
        "--hidden-import=PyQt5.QtWidgets",
        "--hidden-import=PyQt5.sip",
        "--collect-submodules=PyQt5",
        f"--distpath={dist_dir}",
        f"--workpath={build_dir}",
        f"--specpath={script_dir}",
        "--strip",             # Strip binary (smaller size)
        "--optimize=2",        # Optimize Python bytecode
        str(main_script)
    ]
    
    print("Building executable...")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True)
        
        # Verify the executable was created (no .exe extension on Linux)
        exe_name = 'BreakReminder.exe' if os.name == 'nt' else 'BreakReminder'
        exe_path = dist_dir / exe_name
        if exe_path.exists():
            print("\\nBuild completed successfully!")
            print(f"Executable created at: {exe_path}")
            print(f"Executable size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
            
            # Create a simple installer bat file (Windows only)
            if os.name == 'nt':
                create_installer_bat()
        else:
            print("\\nBuild completed, but executable not found!")
            print(f"Expected: {exe_path}")
            sys.exit(1)
        
    except subprocess.CalledProcessError as e:
        print(f"\\nBuild failed with error: {e}")
        print("\\nTry installing dependencies first: pip install -r requirements.txt")
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