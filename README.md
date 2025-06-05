# breaktime

## Installation

1. Install Python 3.x from https://www.python.org/
2. Install dependencies:
   ```powershell
   pip install PyQt5
   ```
3. (Optional) To create a Windows .exe, install PyInstaller:
   ```powershell
   pip install pyinstaller
   pyinstaller --onefile --noconsole break_reminder.py
   ```
   The .exe will appear in the `dist` folder.

## Usage

Run the script:
```powershell
python break_reminder.py
```
Or double-click the generated `.exe`.

## Features

- Overlay reminder in the top-right corner of your screen.
- Reminds you of breaks and lunch during your workday.
- Lunch break window and start time are customizable.
- Remembers your preferred ("usual") start and lunch times.

## Setting Start and Lunch Times

When you start the program, you will be asked:

- Use your usual start/lunch times (pre-filled from last time), or
- Edit the times for today (and optionally save them as your new usual times).

You can always edit your preferred times at launch. The app stores your preferences in a `.break_reminder_config.json` file in your home directory.

