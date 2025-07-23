# Break Reminder - Enhanced Edition

A modern break reminder application with improved visual styling, enhanced usability, and modular architecture.

## ✨ Features

### Core Functionality
- **Smart Break Reminders**: Automatically reminds you of breaks at 25% and 75% of your workday
- **Flexible Lunch Breaks**: Customizable lunch break window with countdown timer
- **Workday Completion**: Celebrates when your workday is complete with fun Finnish messages
- **Configurable Schedule**: Set your own start times, lunch periods, and workday length

### Enhanced UI & UX
- **Modern Dark & Light Themes**: Choose between sleek dark and clean light themes
- **Smooth Animations**: Animated status indicators and smooth transitions
- **Draggable Interface**: Click and drag the widget anywhere on your screen
- **System Tray Integration**: Minimize to system tray for seamless operation
- **Responsive Design**: Hover effects, visual feedback, and adaptive sizing for different screen DPI
- **Improved Geometry**: Fixed window sizing conflicts and better screen boundary handling

### Advanced Configuration
- **Settings Dialog**: Comprehensive settings with real-time preview
- **Window Positioning**: Place the widget in any corner of your screen
- **Auto-close Timer**: Automatically closes after workday completion
- **Debug Mode**: Toggle detailed timing information
- **Persistent Settings**: All preferences saved automatically

## 🚀 Installation

### Quick Start
1. **Install Python 3.7+** from https://www.python.org/
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application**:
   ```bash
   python break_reminder_enhanced.py
   ```

### Building Executable
Create a standalone executable (Windows/Linux):
```bash
python build.py
```
This will:
- Build a portable single-file executable in the `dist` folder
- Create an installer script for easy deployment (Windows only)
- Bundle all resources for distribution
- Optimize the executable for size and performance

The executable will be named:
- `BreakReminder.exe` on Windows
- `BreakReminder` on Linux/macOS

## 📁 Project Structure

```
breaktime/
├── src/
│   ├── core/
│   │   ├── config.py          # Configuration management
│   │   ├── break_logic.py     # Break timing logic
│   │   └── __init__.py
│   ├── ui/
│   │   ├── main_widget.py     # Main application widget
│   │   ├── config_dialog.py   # Settings dialog
│   │   ├── styles.py          # Theme and styling
│   │   └── __init__.py
│   ├── utils/
│   │   └── __init__.py
│   ├── main.py                # Application entry point
│   └── __init__.py
├── break_reminder_enhanced.py  # Main launcher script
├── build.py                   # Build script for executables
├── requirements.txt           # Python dependencies
├── break_reminder.py          # Legacy version (preserved)
└── README.md                  # This file
```

## ⚙️ Configuration

### Settings Dialog
Access comprehensive settings through:
- Click the ⚙️ settings button in the widget
- Right-click context menu → Settings
- System tray → Settings

### Configuration Options
- **Work Schedule**: Start time, lunch periods, workday length
- **Appearance**: Dark/light theme, window position
- **Behavior**: Auto-close timer, notifications, startup options

### Configuration File
Settings are stored in `~/.break_reminder_config.json` with options for:
```json
{
  "usual_start": "08:00",
  "lunch_start": "10:45",
  "lunch_end": "12:30",
  "workday_length": "08:00",
  "theme": "dark",
  "window_position": "top-right",
  "auto_close_delay": 30,
  "notifications_enabled": true,
  "start_minimized": false,
  "debug_mode": false
}
```

## 🎨 Themes

### Dark Theme (Default)
- Sleek dark gradients with blue accents
- High contrast for comfortable viewing
- Subtle animations and hover effects

### Light Theme
- Clean white interface with blue highlights
- Perfect for bright environments
- Consistent with system light mode

## 🖱️ Usage

### Main Widget
- **Drag to Move**: Click and drag anywhere on the widget
- **Status Indicator**: Animated dot shows current state (work/break/lunch/done)
- **Debug Mode**: Toggle detailed timing information
- **Settings**: Configure all options through modern dialog

### System Tray
- **Minimize to Tray**: Continue running in background
- **Quick Access**: Double-click to show/hide widget
- **Context Menu**: Access settings and controls

### Keyboard Shortcuts
- **Right-click**: Context menu with theme switching and settings
- **Drag**: Move widget to any screen position
- **Hover**: Visual feedback and enhanced appearance

## 🔧 Development

### Code Architecture
- **Modular Design**: Clean separation of concerns
- **Modern Python**: Type hints and proper error handling
- **PyQt5 Integration**: Native system integration
- **Extensible**: Easy to add new features and themes

### Adding New Themes
1. Edit `src/ui/styles.py`
2. Add new theme method to `StyleManager`
3. Update theme selection in configuration

### Building from Source
```bash
# Install development dependencies
pip install -r requirements.txt

# Run in development mode
python break_reminder_enhanced.py

# Build standalone executable
python build.py
```

## 📋 Requirements

- **Python**: 3.7 or higher
- **PyQt5**: 5.15.0 or higher
- **PyInstaller**: 6.0.0 or higher (for building executables)
- **Operating System**: Windows 10/11 (primary), Linux, macOS

## 🤝 Contributing

Feel free to contribute improvements:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🎉 Acknowledgments

- Modern UI inspired by contemporary design principles
- Finnish humor for workday completion messages
- Built with PyQt5 for cross-platform compatibility

