"""Configuration dialog for Break Reminder application."""

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                            QLabel, QLineEdit, QPushButton, QComboBox,
                            QCheckBox, QSpinBox, QMessageBox)
from PyQt5.QtCore import Qt

from ..core.config import ConfigManager
from ..ui.styles import StyleManager, Theme


class ConfigDialog(QDialog):
    """Enhanced configuration dialog with modern UI."""
    
    def __init__(self, config_manager: ConfigManager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.style_manager = StyleManager(Theme(config_manager.get("theme", "dark")))
        
        self.init_ui()
        self.load_values()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("⚙️ Break Reminder Settings")
        self.setFixedSize(500, 600)
        self.setModal(True)
        
        # Apply styling
        self.setStyleSheet(self.style_manager.get_style("dialog_base"))
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(24)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("Configure Your Work Schedule")
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #3182ce;
            margin-bottom: 16px;
        """)
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Create form sections
        self.create_time_section(main_layout)
        self.create_appearance_section(main_layout)
        self.create_behavior_section(main_layout)
        
        # Buttons
        self.create_buttons(main_layout)
        
        self.setLayout(main_layout)
    
    def create_time_section(self, main_layout):
        """Create time configuration section."""
        # Time section
        time_group = QtWidgets.QGroupBox("⏰ Work Schedule")
        time_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                margin-top: 12px;
                padding-top: 12px;
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px;
                color: #3182ce;
            }
        """)
        
        time_layout = QFormLayout()
        time_layout.setSpacing(16)
        time_layout.setVerticalSpacing(12)
        
        # Input fields
        self.start_time_edit = QLineEdit()
        self.start_time_edit.setPlaceholderText("e.g., 08:00")
        self.start_time_edit.setStyleSheet(self.style_manager.get_style("dialog_input"))
        
        self.lunch_start_edit = QLineEdit()
        self.lunch_start_edit.setPlaceholderText("e.g., 11:00")
        self.lunch_start_edit.setStyleSheet(self.style_manager.get_style("dialog_input"))
        
        self.lunch_end_edit = QLineEdit()
        self.lunch_end_edit.setPlaceholderText("e.g., 12:00")
        self.lunch_end_edit.setStyleSheet(self.style_manager.get_style("dialog_input"))
        
        self.workday_length_edit = QLineEdit()
        self.workday_length_edit.setPlaceholderText("e.g., 08:00")
        self.workday_length_edit.setStyleSheet(self.style_manager.get_style("dialog_input"))
        
        # Labels
        label_style = self.style_manager.get_style("dialog_label")
        
        time_layout.addRow(self.create_label("🚀 Start time (HH:MM):", label_style), self.start_time_edit)
        time_layout.addRow(self.create_label("🍽️ Lunch start (HH:MM):", label_style), self.lunch_start_edit)
        time_layout.addRow(self.create_label("🍽️ Lunch end (HH:MM):", label_style), self.lunch_end_edit)
        time_layout.addRow(self.create_label("⏰ Workday length (HH:MM):", label_style), self.workday_length_edit)
        
        time_group.setLayout(time_layout)
        main_layout.addWidget(time_group)
    
    def create_appearance_section(self, main_layout):
        """Create appearance configuration section."""
        appearance_group = QtWidgets.QGroupBox("🎨 Appearance")
        appearance_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                margin-top: 12px;
                padding-top: 12px;
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px;
                color: #3182ce;
            }
        """)
        
        appearance_layout = QFormLayout()
        appearance_layout.setSpacing(16)
        appearance_layout.setVerticalSpacing(12)
        
        # Theme selection
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light"])
        self.theme_combo.setStyleSheet(self.style_manager.get_style("dialog_input"))
        
        # Window position
        self.position_combo = QComboBox()
        self.position_combo.addItems(["Top Right", "Top Left", "Bottom Right", "Bottom Left"])
        self.position_combo.setStyleSheet(self.style_manager.get_style("dialog_input"))
        
        # Labels
        label_style = self.style_manager.get_style("dialog_label")
        
        appearance_layout.addRow(self.create_label("🌓 Theme:", label_style), self.theme_combo)
        appearance_layout.addRow(self.create_label("📍 Window position:", label_style), self.position_combo)
        
        appearance_group.setLayout(appearance_layout)
        main_layout.addWidget(appearance_group)
    
    def create_behavior_section(self, main_layout):
        """Create behavior configuration section."""
        behavior_group = QtWidgets.QGroupBox("⚙️ Behavior")
        behavior_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                margin-top: 12px;
                padding-top: 12px;
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px;
                color: #3182ce;
            }
        """)
        
        behavior_layout = QFormLayout()
        behavior_layout.setSpacing(16)
        behavior_layout.setVerticalSpacing(12)
        
        # Auto-close delay
        self.auto_close_spin = QSpinBox()
        self.auto_close_spin.setRange(1, 120)
        self.auto_close_spin.setSuffix(" minutes")
        self.auto_close_spin.setStyleSheet(self.style_manager.get_style("dialog_input"))
        
        # Checkboxes
        checkbox_style = """
            QCheckBox {
                color: #e2e8f0;
                font-size: 14px;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 3px;
                background: rgba(255, 255, 255, 0.05);
            }
            QCheckBox::indicator:checked {
                background: #3182ce;
                border-color: #3182ce;
            }
            QCheckBox::indicator:checked::before {
                content: "✓";
                color: white;
                font-weight: bold;
            }
        """
        
        self.notifications_check = QCheckBox("Enable notifications")
        self.notifications_check.setStyleSheet(checkbox_style)
        
        self.sound_check = QCheckBox("Enable sound alerts")
        self.sound_check.setStyleSheet(checkbox_style)
        
        self.start_minimized_check = QCheckBox("Start minimized")
        self.start_minimized_check.setStyleSheet(checkbox_style)
        
        # Labels
        label_style = self.style_manager.get_style("dialog_label")
        
        behavior_layout.addRow(self.create_label("🔔 Auto-close after workday:", label_style), self.auto_close_spin)
        behavior_layout.addRow(self.notifications_check)
        behavior_layout.addRow(self.sound_check)
        behavior_layout.addRow(self.start_minimized_check)
        
        behavior_group.setLayout(behavior_layout)
        main_layout.addWidget(behavior_group)
    
    def create_buttons(self, main_layout):
        """Create dialog buttons."""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        # Reset to defaults button
        self.reset_btn = QPushButton("🔄 Reset to Defaults")
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6c757d, stop:1 #495057);
                border: none;
                color: white;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 14px;
                min-width: 120px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5a6268, stop:1 #3d4142);
            }
            QPushButton:pressed {
                background: #3d4142;
            }
        """)
        self.reset_btn.clicked.connect(self.reset_to_defaults)
        
        # Cancel button
        self.cancel_btn = QPushButton("❌ Cancel")
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6c757d, stop:1 #495057);
                border: none;
                color: white;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5a6268, stop:1 #3d4142);
            }
            QPushButton:pressed {
                background: #3d4142;
            }
        """)
        self.cancel_btn.clicked.connect(self.reject)
        
        # OK button
        self.ok_btn = QPushButton("✅ Apply Settings")
        self.ok_btn.setStyleSheet(self.style_manager.get_style("dialog_button"))
        self.ok_btn.clicked.connect(self.accept_settings)
        
        button_layout.addWidget(self.reset_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.ok_btn)
        
        main_layout.addLayout(button_layout)
    
    def create_label(self, text: str, style: str) -> QLabel:
        """Create a styled label.
        
        Args:
            text: Label text
            style: CSS style string
            
        Returns:
            Configured QLabel
        """
        label = QLabel(text)
        label.setStyleSheet(style)
        return label
    
    def load_values(self):
        """Load current configuration values into the form."""
        config = self.config_manager.get_all()
        
        # Time settings
        self.start_time_edit.setText(config.get("usual_start", "08:00"))
        self.lunch_start_edit.setText(config.get("lunch_start", "10:45"))
        self.lunch_end_edit.setText(config.get("lunch_end", "12:30"))
        self.workday_length_edit.setText(config.get("workday_length", "08:00"))
        
        # Appearance settings
        theme = config.get("theme", "dark")
        self.theme_combo.setCurrentText("Dark" if theme == "dark" else "Light")
        
        position = config.get("window_position", "top-right")
        position_map = {
            "top-right": "Top Right",
            "top-left": "Top Left", 
            "bottom-right": "Bottom Right",
            "bottom-left": "Bottom Left"
        }
        self.position_combo.setCurrentText(position_map.get(position, "Top Right"))
        
        # Behavior settings
        self.auto_close_spin.setValue(config.get("auto_close_delay", 30))
        self.notifications_check.setChecked(config.get("notifications_enabled", True))
        self.sound_check.setChecked(config.get("sound_enabled", False))
        self.start_minimized_check.setChecked(config.get("start_minimized", False))
    
    def accept_settings(self):
        """Validate and accept the settings."""
        try:
            # Validate time formats
            self.validate_time_format(self.start_time_edit.text(), "Start time")
            self.validate_time_format(self.lunch_start_edit.text(), "Lunch start")
            self.validate_time_format(self.lunch_end_edit.text(), "Lunch end")
            self.validate_time_format(self.workday_length_edit.text(), "Workday length")
            
            # Save settings
            self.save_settings()
            
            # Show success message
            QMessageBox.information(self, "Success", "Settings saved successfully!")
            
            self.accept()
            
        except ValueError as e:
            QMessageBox.warning(self, "Invalid Input", str(e))
    
    def validate_time_format(self, time_str: str, field_name: str):
        """Validate time format.
        
        Args:
            time_str: Time string to validate
            field_name: Name of the field for error messages
            
        Raises:
            ValueError: If time format is invalid
        """
        if not time_str:
            raise ValueError(f"{field_name} cannot be empty")
        
        if ":" not in time_str:
            raise ValueError(f"{field_name} must be in HH:MM format")
        
        try:
            hours, minutes = map(int, time_str.split(":"))
            if hours < 0 or hours > 23:
                raise ValueError(f"{field_name} hours must be between 0 and 23")
            if minutes < 0 or minutes > 59:
                raise ValueError(f"{field_name} minutes must be between 0 and 59")
        except ValueError:
            raise ValueError(f"{field_name} must be in HH:MM format with valid numbers")
    
    def save_settings(self):
        """Save the current form values to configuration."""
        # Time settings
        self.config_manager.set("usual_start", self.start_time_edit.text())
        self.config_manager.set("lunch_start", self.lunch_start_edit.text())
        self.config_manager.set("lunch_end", self.lunch_end_edit.text())
        self.config_manager.set("workday_length", self.workday_length_edit.text())
        
        # Appearance settings
        theme = "dark" if self.theme_combo.currentText() == "Dark" else "light"
        self.config_manager.set("theme", theme)
        
        position_map = {
            "Top Right": "top-right",
            "Top Left": "top-left",
            "Bottom Right": "bottom-right",
            "Bottom Left": "bottom-left"
        }
        position = position_map.get(self.position_combo.currentText(), "top-right")
        self.config_manager.set("window_position", position)
        
        # Behavior settings
        self.config_manager.set("auto_close_delay", self.auto_close_spin.value())
        self.config_manager.set("notifications_enabled", self.notifications_check.isChecked())
        self.config_manager.set("sound_enabled", self.sound_check.isChecked())
        self.config_manager.set("start_minimized", self.start_minimized_check.isChecked())
        
        # Save to file
        self.config_manager.save()
    
    def reset_to_defaults(self):
        """Reset all settings to default values."""
        reply = QMessageBox.question(
            self, 
            "Reset to Defaults",
            "Are you sure you want to reset all settings to their default values?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.config_manager.reset_to_defaults()
            self.config_manager.save()
            self.load_values()
            QMessageBox.information(self, "Success", "Settings reset to defaults!")