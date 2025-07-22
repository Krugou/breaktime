"""Modern UI styles and themes for Break Reminder application."""

from enum import Enum
from typing import Dict, Any


class Theme(Enum):
    """Available themes for the application."""
    DARK = "dark"
    LIGHT = "light"
    AUTO = "auto"


class StyleManager:
    """Manages application styles and themes."""
    
    def __init__(self, theme: Theme = Theme.DARK):
        """Initialize style manager.
        
        Args:
            theme: Theme to use for styling
        """
        self.theme = theme
        self._styles = self._load_styles()
    
    def _load_styles(self) -> Dict[str, Dict[str, str]]:
        """Load all available styles.
        
        Returns:
            Dictionary of style definitions
        """
        return {
            "dark": self._get_dark_theme(),
            "light": self._get_light_theme(),
        }
    
    def _get_dark_theme(self) -> Dict[str, str]:
        """Get dark theme styles.
        
        Returns:
            Dictionary of dark theme styles
        """
        return {
            "main_window": """
                QWidget {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(45, 45, 55, 240),
                        stop:1 rgba(25, 25, 35, 240));
                    border-radius: 15px;
                    border: 2px solid rgba(100, 100, 120, 80);
                }
            """,
            "main_window_hover": """
                QWidget {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(55, 55, 65, 250),
                        stop:1 rgba(35, 35, 45, 250));
                    border-radius: 15px;
                    border: 2px solid rgba(120, 120, 140, 120);
                }
            """,
            "main_label": """
                QLabel {
                    color: #ffffff;
                    font-size: 16px;
                    font-weight: 500;
                    font-family: 'Segoe UI', 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif;
                    padding: 16px 20px;
                    background: transparent;
                    border: none;
                }
            """,
            "title_label": """
                QLabel {
                    color: rgba(255, 255, 255, 200);
                    font-size: 12px;
                    font-weight: 600;
                    font-family: 'Segoe UI', 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif;
                    background: transparent;
                    border: none;
                }
            """,
            "button_base": """
                QPushButton {
                    border: none;
                    border-radius: 16px;
                    font-weight: 600;
                    font-size: 14px;
                    font-family: 'Segoe UI', 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif;
                    padding: 8px 16px;
                }
            """,
            "debug_button": """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(255, 193, 7, 180),
                        stop:1 rgba(255, 159, 0, 180));
                    color: #212529;
                    border: 1px solid rgba(255, 193, 7, 100);
                    border-radius: 16px;
                    font-size: 14px;
                    font-weight: 600;
                    min-width: 32px;
                    min-height: 32px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(255, 193, 7, 220),
                        stop:1 rgba(255, 159, 0, 220));
                    border: 1px solid rgba(255, 193, 7, 150);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(255, 159, 0, 200),
                        stop:1 rgba(255, 111, 0, 200));
                }
                QPushButton:checked {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(255, 224, 102, 255),
                        stop:1 rgba(255, 193, 7, 255));
                    color: #000000;
                }
            """,
            "close_button": """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(220, 53, 69, 180),
                        stop:1 rgba(185, 28, 28, 180));
                    color: white;
                    border: 1px solid rgba(220, 53, 69, 100);
                    border-radius: 16px;
                    font-weight: 700;
                    font-size: 16px;
                    min-width: 32px;
                    min-height: 32px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(220, 53, 69, 220),
                        stop:1 rgba(185, 28, 28, 220));
                    border: 1px solid rgba(220, 53, 69, 150);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(185, 28, 28, 200),
                        stop:1 rgba(153, 27, 27, 200));
                }
            """,
            "settings_button": """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(108, 117, 125, 180),
                        stop:1 rgba(73, 80, 87, 180));
                    color: white;
                    border: 1px solid rgba(108, 117, 125, 100);
                    border-radius: 16px;
                    font-weight: 600;
                    font-size: 14px;
                    min-width: 32px;
                    min-height: 32px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(108, 117, 125, 220),
                        stop:1 rgba(73, 80, 87, 220));
                    border: 1px solid rgba(108, 117, 125, 150);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(73, 80, 87, 200),
                        stop:1 rgba(52, 58, 64, 200));
                }
            """,
            "dialog_base": """
                QDialog {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #2d3748, stop:1 #1a202c);
                    border-radius: 12px;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    font-family: 'Segoe UI', 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif;
                }
            """,
            "dialog_label": """
                QLabel {
                    color: #e2e8f0;
                    font-weight: 500;
                    font-size: 14px;
                    margin: 4px 0;
                }
            """,
            "dialog_input": """
                QLineEdit {
                    border: 2px solid rgba(255, 255, 255, 0.1);
                    border-radius: 8px;
                    padding: 12px 16px;
                    font-size: 16px;
                    background: rgba(255, 255, 255, 0.05);
                    color: #ffffff;
                    selection-background-color: #3182ce;
                    min-height: 20px;
                }
                QLineEdit:focus {
                    border-color: #3182ce;
                    background: rgba(255, 255, 255, 0.08);
                    outline: none;
                }
                QLineEdit::placeholder {
                    color: rgba(255, 255, 255, 0.5);
                }
            """,
            "dialog_button": """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #3182ce, stop:1 #2c5aa0);
                    border: none;
                    color: white;
                    padding: 12px 24px;
                    border-radius: 8px;
                    font-weight: 600;
                    font-size: 14px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #2c5aa0, stop:1 #2a4d8d);
                }
                QPushButton:pressed {
                    background: #2a4d8d;
                }
            """,
            "progress_bar": """
                QProgressBar {
                    border: none;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 8px;
                    height: 16px;
                    text-align: center;
                    font-size: 11px;
                    font-weight: 600;
                    font-family: 'Segoe UI', 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif;
                    color: rgba(255, 255, 255, 0.8);
                }
                QProgressBar::chunk {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgba(16, 185, 129, 200),
                        stop:1 rgba(5, 150, 105, 200));
                    border-radius: 8px;
                    border: none;
                }
                QProgressBar[breakState="work"]::chunk {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgba(16, 185, 129, 200),
                        stop:1 rgba(5, 150, 105, 200));
                }
                QProgressBar[breakState="break"]::chunk {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgba(245, 158, 11, 200),
                        stop:1 rgba(217, 119, 6, 200));
                }
                QProgressBar[breakState="lunch"]::chunk {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgba(59, 130, 246, 200),
                        stop:1 rgba(37, 99, 235, 200));
                }
                QProgressBar[breakState="done"]::chunk {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgba(139, 92, 246, 200),
                        stop:1 rgba(124, 58, 237, 200));
                }
            """,
            "status_colors": {
                "work": "#10b981",      # Emerald
                "break": "#f59e0b",     # Amber
                "lunch": "#3b82f6",     # Blue
                "done": "#8b5cf6"       # Violet
            }
        }
    
    def _get_light_theme(self) -> Dict[str, str]:
        """Get light theme styles.
        
        Returns:
            Dictionary of light theme styles
        """
        return {
            "main_window": """
                QWidget {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(255, 255, 255, 240),
                        stop:1 rgba(248, 249, 250, 240));
                    border-radius: 15px;
                    border: 2px solid rgba(200, 200, 210, 120);
                }
            """,
            "main_window_hover": """
                QWidget {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(255, 255, 255, 250),
                        stop:1 rgba(248, 249, 250, 250));
                    border-radius: 15px;
                    border: 2px solid rgba(180, 180, 190, 150);
                }
            """,
            "main_label": """
                QLabel {
                    color: #1a202c;
                    font-size: 16px;
                    font-weight: 500;
                    font-family: 'Segoe UI', 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif;
                    padding: 16px 20px;
                    background: transparent;
                    border: none;
                }
            """,
            "title_label": """
                QLabel {
                    color: rgba(26, 32, 44, 180);
                    font-size: 12px;
                    font-weight: 600;
                    font-family: 'Segoe UI', 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif;
                    background: transparent;
                    border: none;
                }
            """,
            "button_base": """
                QPushButton {
                    border: none;
                    border-radius: 16px;
                    font-weight: 600;
                    font-size: 14px;
                    font-family: 'Segoe UI', 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif;
                    padding: 8px 16px;
                }
            """,
            "debug_button": """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(255, 193, 7, 200),
                        stop:1 rgba(255, 159, 0, 200));
                    color: #212529;
                    border: 1px solid rgba(255, 193, 7, 120);
                    border-radius: 16px;
                    font-size: 14px;
                    font-weight: 600;
                    min-width: 32px;
                    min-height: 32px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(255, 193, 7, 240),
                        stop:1 rgba(255, 159, 0, 240));
                    border: 1px solid rgba(255, 193, 7, 170);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(255, 159, 0, 220),
                        stop:1 rgba(255, 111, 0, 220));
                }
                QPushButton:checked {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(255, 224, 102, 255),
                        stop:1 rgba(255, 193, 7, 255));
                    color: #000000;
                }
            """,
            "close_button": """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(220, 53, 69, 200),
                        stop:1 rgba(185, 28, 28, 200));
                    color: white;
                    border: 1px solid rgba(220, 53, 69, 120);
                    border-radius: 16px;
                    font-weight: 700;
                    font-size: 16px;
                    min-width: 32px;
                    min-height: 32px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(220, 53, 69, 240),
                        stop:1 rgba(185, 28, 28, 240));
                    border: 1px solid rgba(220, 53, 69, 170);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(185, 28, 28, 220),
                        stop:1 rgba(153, 27, 27, 220));
                }
            """,
            "settings_button": """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(108, 117, 125, 200),
                        stop:1 rgba(73, 80, 87, 200));
                    color: white;
                    border: 1px solid rgba(108, 117, 125, 120);
                    border-radius: 16px;
                    font-weight: 600;
                    font-size: 14px;
                    min-width: 32px;
                    min-height: 32px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(108, 117, 125, 240),
                        stop:1 rgba(73, 80, 87, 240));
                    border: 1px solid rgba(108, 117, 125, 170);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(73, 80, 87, 220),
                        stop:1 rgba(52, 58, 64, 220));
                }
            """,
            "dialog_base": """
                QDialog {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #ffffff, stop:1 #f8f9fa);
                    border-radius: 12px;
                    border: 1px solid rgba(0, 0, 0, 0.1);
                    font-family: 'Segoe UI', 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif;
                }
            """,
            "dialog_label": """
                QLabel {
                    color: #495057;
                    font-weight: 500;
                    font-size: 14px;
                    margin: 4px 0;
                }
            """,
            "dialog_input": """
                QLineEdit {
                    border: 2px solid #dee2e6;
                    border-radius: 8px;
                    padding: 12px 16px;
                    font-size: 16px;
                    background: white;
                    color: #495057;
                    selection-background-color: #007bff;
                    min-height: 20px;
                }
                QLineEdit:focus {
                    border-color: #007bff;
                    outline: none;
                }
                QLineEdit::placeholder {
                    color: #6c757d;
                }
            """,
            "dialog_button": """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #007bff, stop:1 #0056b3);
                    border: none;
                    color: white;
                    padding: 12px 24px;
                    border-radius: 8px;
                    font-weight: 600;
                    font-size: 14px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #0056b3, stop:1 #004085);
                }
                QPushButton:pressed {
                    background: #004085;
                }
            """,
            "progress_bar": """
                QProgressBar {
                    border: 1px solid rgba(0, 0, 0, 0.1);
                    background: rgba(0, 0, 0, 0.05);
                    border-radius: 8px;
                    height: 16px;
                    text-align: center;
                    font-size: 11px;
                    font-weight: 600;
                    font-family: 'Segoe UI', 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif;
                    color: rgba(0, 0, 0, 0.7);
                }
                QProgressBar::chunk {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgba(5, 150, 105, 220),
                        stop:1 rgba(4, 120, 87, 220));
                    border-radius: 8px;
                    border: none;
                }
                QProgressBar[breakState="work"]::chunk {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgba(5, 150, 105, 220),
                        stop:1 rgba(4, 120, 87, 220));
                }
                QProgressBar[breakState="break"]::chunk {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgba(217, 119, 6, 220),
                        stop:1 rgba(180, 83, 9, 220));
                }
                QProgressBar[breakState="lunch"]::chunk {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgba(37, 99, 235, 220),
                        stop:1 rgba(29, 78, 216, 220));
                }
                QProgressBar[breakState="done"]::chunk {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgba(124, 58, 237, 220),
                        stop:1 rgba(109, 40, 217, 220));
                }
            """,
            "status_colors": {
                "work": "#059669",      # Emerald
                "break": "#d97706",     # Amber  
                "lunch": "#2563eb",     # Blue
                "done": "#7c3aed"       # Violet
            }
        }
    
    def get_style(self, element: str) -> str:
        """Get style for a specific element.
        
        Args:
            element: Element name to get style for
            
        Returns:
            CSS style string
        """
        theme_name = self.theme.value
        if theme_name == "auto":
            # For now, default to dark theme for auto
            theme_name = "dark"
        
        return self._styles.get(theme_name, {}).get(element, "")
    
    def get_status_color(self, status: str) -> str:
        """Get color for a specific status.
        
        Args:
            status: Status name (work, break, lunch, done)
            
        Returns:
            Color hex code
        """
        theme_name = self.theme.value
        if theme_name == "auto":
            theme_name = "dark"
        
        colors = self._styles.get(theme_name, {}).get("status_colors", {})
        return colors.get(status, "#ffffff")
    
    def set_theme(self, theme: Theme) -> None:
        """Set the active theme.
        
        Args:
            theme: Theme to set
        """
        self.theme = theme