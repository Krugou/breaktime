"""Main application entry point for Break Reminder."""

import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QMessageBox
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon

from .core.config import ConfigManager
from .ui.main_widget import BreakReminderWidget
from .ui.config_dialog import ConfigDialog


class BreakReminderApp:
    """Main application class with system tray support."""
    
    def __init__(self):
        """Initialize the application."""
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)  # Keep running in system tray
        
        # Initialize configuration
        self.config_manager = ConfigManager()
        
        # Initialize main widget
        self.main_widget = None
        
        # Initialize system tray
        self.init_system_tray()
        
        # Show main widget or start minimized
        if not self.config_manager.get("start_minimized", False):
            self.show_main_widget()
    
    def init_system_tray(self):
        """Initialize system tray icon and menu."""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            QMessageBox.critical(
                None, 
                "System Tray",
                "System tray is not available on this system."
            )
            return
        
        # Create system tray icon
        self.tray_icon = QSystemTrayIcon(self.app)
        
        # Set icon (you can replace this with a custom icon)
        self.tray_icon.setIcon(self.app.style().standardIcon(
            self.app.style().SP_ComputerIcon
        ))
        
        # Create context menu
        self.create_tray_menu()
        
        # Set tooltip
        self.tray_icon.setToolTip("Break Reminder")
        
        # Handle double-click
        self.tray_icon.activated.connect(self.tray_icon_activated)
        
        # Show the tray icon
        self.tray_icon.show()
    
    def create_tray_menu(self):
        """Create system tray context menu."""
        menu = QMenu()
        
        # Show/Hide action
        self.show_action = QAction("Show Break Reminder", self.app)
        self.show_action.triggered.connect(self.show_main_widget)
        menu.addAction(self.show_action)
        
        # Settings action
        settings_action = QAction("Settings", self.app)
        settings_action.triggered.connect(self.show_settings)
        menu.addAction(settings_action)
        
        menu.addSeparator()
        
        # About action
        about_action = QAction("About", self.app)
        about_action.triggered.connect(self.show_about)
        menu.addAction(about_action)
        
        # Quit action
        quit_action = QAction("Quit", self.app)
        quit_action.triggered.connect(self.quit_application)
        menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(menu)
    
    def tray_icon_activated(self, reason):
        """Handle system tray icon activation.
        
        Args:
            reason: Activation reason
        """
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_main_widget()
    
    def show_main_widget(self):
        """Show the main widget."""
        if self.main_widget is None:
            self.main_widget = BreakReminderWidget(self.config_manager)
        
        self.main_widget.show()
        self.main_widget.raise_()
        self.main_widget.activateWindow()
        
        # Update tray menu
        self.show_action.setText("Hide Break Reminder")
        self.show_action.triggered.disconnect()
        self.show_action.triggered.connect(self.hide_main_widget)
    
    def hide_main_widget(self):
        """Hide the main widget."""
        if self.main_widget is not None:
            self.main_widget.hide()
        
        # Update tray menu
        self.show_action.setText("Show Break Reminder")
        self.show_action.triggered.disconnect()
        self.show_action.triggered.connect(self.show_main_widget)
    
    def show_settings(self):
        """Show settings dialog."""
        dialog = ConfigDialog(self.config_manager)
        if dialog.exec_() == ConfigDialog.Accepted:
            # If main widget exists, update it
            if self.main_widget is not None:
                self.main_widget.break_logic.update_config(self.config_manager.get_all())
                self.main_widget.update_display()
    
    def show_about(self):
        """Show about dialog."""
        from . import __version__, __description__
        
        msg = QMessageBox()
        msg.setWindowTitle("About Break Reminder")
        msg.setIcon(QMessageBox.Information)
        msg.setText(f"""
        <h3>Break Reminder</h3>
        <p><b>Version:</b> {__version__}</p>
        <p><b>Description:</b> {__description__}</p>
        <p>A modern break reminder application built with PyQt5.</p>
        <p>Helps you maintain a healthy work-life balance with timely break reminders.</p>
        """)
        msg.exec_()
    
    def quit_application(self):
        """Quit the application."""
        if self.main_widget is not None:
            self.main_widget.close()
        self.tray_icon.hide()
        self.app.quit()
    
    def run(self):
        """Run the application."""
        return self.app.exec_()


def main():
    """Main entry point."""
    app = BreakReminderApp()
    return app.run()


if __name__ == "__main__":
    sys.exit(main())