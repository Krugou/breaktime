"""Main break reminder widget with enhanced UI."""

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QPointF, Qt
from PyQt5.QtGui import QColor, QCursor, QFont
from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QGraphicsDropShadowEffect, QApplication, QProgressBar)

from ..core.break_logic import BreakLogic, BreakState
from ..core.config import ConfigManager
from ..ui.styles import StyleManager, Theme
from .config_dialog import ConfigDialog


class StatusIndicator(QLabel):
    """Animated status indicator widget."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(20, 20)
        self.setAlignment(Qt.AlignCenter)
        self.setText('●')
        self.setStyleSheet("""
            font-size: 24px;
            background: transparent;
            border: none;
        """)
        
        # Animation for pulsing effect
        self.animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(1000)
        self.animation.setLoopCount(-1)
        
        # Opacity animation
        self.opacity_effect = QtWidgets.QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)
        
        self.opacity_animation = QtCore.QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_animation.setDuration(2000)
        self.opacity_animation.setStartValue(0.6)
        self.opacity_animation.setEndValue(1.0)
        self.opacity_animation.setLoopCount(-1)
        
        # Easing curve for smooth animation
        self.opacity_animation.setEasingCurve(QtCore.QEasingCurve.InOutSine)
    
    def update_status(self, state: BreakState, color: str):
        """Update status indicator with new state and color.
        
        Args:
            state: Current break state
            color: Color hex code for the status
        """
        self.setStyleSheet(f"""
            color: {color};
            font-size: 24px;
            background: transparent;
            border: none;
        """)
        
        # Start animation for break and lunch states
        if state in [BreakState.BREAK, BreakState.LUNCH]:
            self.opacity_animation.start()
        else:
            self.opacity_animation.stop()
            self.opacity_effect.setOpacity(1.0)


class BreakReminderWidget(QWidget):
    """Modern break reminder widget with enhanced UI."""
    
    def __init__(self, config_manager: ConfigManager):
        super().__init__()
        self.config_manager = config_manager
        self.style_manager = StyleManager(Theme(config_manager.get("theme", "dark")))
        self.break_logic = BreakLogic(config_manager.get_all())
        
        # Widget state
        self.dragging = False
        self.drag_start_position = None
        self.close_timer_started = False
        
        # Initialize UI
        self.init_ui()
        
        # Setup update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_display)
        self.update_timer.start(60000)  # Update every minute
        
        # Initial update
        self.update_display()
    
    def init_ui(self):
        """Initialize the user interface."""
        # Window properties
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Main container
        self.container = QWidget()
        self.container.setStyleSheet(self.style_manager.get_style("main_window"))
        self.container.setCursor(Qt.OpenHandCursor)
        
        # Create UI components
        self.create_status_indicator()
        self.create_labels()
        self.create_progress_bar()
        self.create_buttons()
        self.create_layout()
        
        # Window setup with responsive sizing
        self.setMinimumSize(380, 140)
        self.setMaximumSize(520, 260)
        self.resize(400, 160)
        self.position_window()
        self.add_drop_shadow()
        
        # Tooltip for drag functionality
        self.setToolTip("💡 Click and drag to move • Right-click for options")
    
    def create_status_indicator(self):
        """Create animated status indicator with improved size."""
        self.status_indicator = StatusIndicator(self)
        # Make status indicator larger for better visibility
        self.status_indicator.setFixedSize(20, 20)
    
    def create_labels(self):
        """Create text labels."""
        # Main content label
        self.main_label = QLabel('')
        self.main_label.setStyleSheet(self.style_manager.get_style("main_label"))
        self.main_label.setWordWrap(True)
        self.main_label.setAlignment(Qt.AlignCenter)
        self.main_label.setMinimumHeight(40)
        self.main_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        
        # Title label
        self.title_label = QLabel("Break Reminder")
        self.title_label.setStyleSheet(self.style_manager.get_style("title_label"))
        self.title_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
    
    def create_progress_bar(self):
        """Create progress bar widget with improved height."""
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet(self.style_manager.get_style("progress_bar"))
        self.progress_bar.setFixedHeight(20)  # Increased from 16px for better visibility
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p%")  # Show percentage
    
    def create_buttons(self):
        """Create control buttons with improved sizing."""
        # Debug button - larger for better touch targets
        self.debug_btn = QPushButton('🐞')
        self.debug_btn.setFixedSize(36, 36)
        self.debug_btn.setStyleSheet(self.style_manager.get_style("debug_button"))
        self.debug_btn.setToolTip('Toggle debug information')
        self.debug_btn.setCheckable(True)
        self.debug_btn.setChecked(self.config_manager.get("debug_mode", False))
        self.debug_btn.toggled.connect(self.toggle_debug)
        
        # Settings button
        self.settings_btn = QPushButton('⚙️')
        self.settings_btn.setFixedSize(36, 36)
        self.settings_btn.setStyleSheet(self.style_manager.get_style("settings_button"))
        self.settings_btn.setToolTip('Open settings')
        self.settings_btn.clicked.connect(self.open_settings)
        
        # Close button
        self.close_btn = QPushButton('×')
        self.close_btn.setFixedSize(36, 36)
        self.close_btn.setStyleSheet(self.style_manager.get_style("close_button"))
        self.close_btn.setToolTip('Close application')
        self.close_btn.clicked.connect(self.close)
    
    def create_layout(self):
        """Create and setup the layout with improved spacing."""
        # Main layout with increased margins
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(0)
        
        # Container layout with better spacing
        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(8)
        
        # Header layout with increased margins
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(20, 16, 20, 12)
        header_layout.setSpacing(12)
        
        # Status section with better spacing
        status_section = QHBoxLayout()
        status_section.setSpacing(16)
        status_section.addWidget(self.status_indicator)
        status_section.addWidget(self.title_label)
        status_section.addStretch()
        
        # Controls section with increased spacing
        controls_section = QHBoxLayout()
        controls_section.setSpacing(8)
        controls_section.addWidget(self.debug_btn)
        controls_section.addWidget(self.settings_btn)
        controls_section.addWidget(self.close_btn)
        
        # Assemble header
        header_layout.addLayout(status_section)
        header_layout.addLayout(controls_section)
        
        # Assemble container
        container_layout.addLayout(header_layout)
        container_layout.addWidget(self.main_label)
        
        # Add progress bar with increased margins
        progress_margins = QHBoxLayout()
        progress_margins.setContentsMargins(24, 12, 24, 20)
        progress_margins.addWidget(self.progress_bar)
        container_layout.addLayout(progress_margins)
        
        self.container.setLayout(container_layout)
        
        # Assemble main layout
        main_layout.addWidget(self.container)
        self.setLayout(main_layout)
    
    def position_window(self):
        """Position window based on configuration."""
        screen = QApplication.primaryScreen().geometry()
        position = self.config_manager.get("window_position", "top-right")
        
        margin = 20
        if position == "top-right":
            x = screen.width() - self.width() - margin
            y = margin
        elif position == "top-left":
            x = margin
            y = margin
        elif position == "bottom-right":
            x = screen.width() - self.width() - margin
            y = screen.height() - self.height() - margin
        elif position == "bottom-left":
            x = margin
            y = screen.height() - self.height() - margin
        else:
            # Default to top-right
            x = screen.width() - self.width() - margin
            y = margin
        
        self.move(x, y)
    
    def add_drop_shadow(self):
        """Add drop shadow effect to the container."""
        try:
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(25)
            shadow.setColor(QColor(0, 0, 0, 80))
            shadow.setOffset(QPointF(0, 6))
            self.container.setGraphicsEffect(shadow)
        except:
            # Shadow effect not available, continue without it
            pass
    
    def update_display(self):
        """Update the display with current break information."""
        state, info = self.break_logic.get_current_state()
        
        # Update main message
        message = info["message"]
        if self.config_manager.get("debug_mode", False):
            debug_info = info.get("debug_info", [])
            if debug_info:
                message += "\\n\\n" + "\\n".join(debug_info)
        
        self.main_label.setText(message)
        
        # Update status indicator
        color = self.style_manager.get_status_color(state.value)
        self.status_indicator.update_status(state, color)
        
        # Update progress bar
        progress_percent = info.get("progress_percent", 0)
        self.progress_bar.setValue(progress_percent)
        self.progress_bar.setProperty("breakState", state.value)
        self.progress_bar.setStyleSheet(self.style_manager.get_style("progress_bar"))
        
        # Update progress bar tooltip with more info
        next_event = info.get("next_event", "Unknown")
        time_left = info.get("time_left", 0)
        if time_left > 0:
            self.progress_bar.setToolTip(f"{next_event} in {time_left} minutes ({progress_percent}% complete)")
        else:
            self.progress_bar.setToolTip(f"{next_event} ({progress_percent}% complete)")
        
        # Adjust window size based on content
        self.adjust_window_size()
        
        # Handle workday completion
        if state == BreakState.DONE and not self.close_timer_started:
            self.close_timer_started = True
            auto_close_delay = self.config_manager.get("auto_close_delay", 30)
            QTimer.singleShot(auto_close_delay * 60 * 1000, self.close)
    
    def adjust_window_size(self):
        """Dynamically adjust window size based on content with improved spacing."""
        # Get the preferred size for the main label
        fm = self.main_label.fontMetrics()
        text_rect = fm.boundingRect(
            0, 0, 450, 240,  # Increased maximum width and height
            Qt.TextWordWrap | Qt.AlignCenter,
            self.main_label.text()
        )
        
        # Calculate required height based on text with more generous spacing  
        required_height = max(140, text_rect.height() + 100)  # 100px for header, progress bar, and margins
        required_height = min(required_height, 260)  # Don't exceed maximum
        
        # Resize if needed
        if self.height() != required_height:
            self.resize(self.width(), required_height)
    
    def toggle_debug(self, checked):
        """Toggle debug mode display.
        
        Args:
            checked: Whether debug mode is enabled
        """
        self.config_manager.set("debug_mode", checked)
        self.config_manager.save()
        self.update_display()
    
    def open_settings(self):
        """Open the settings dialog."""
        dialog = ConfigDialog(self.config_manager, self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            # Update break logic with new configuration
            self.break_logic.update_config(self.config_manager.get_all())
            
            # Update theme if changed
            new_theme = Theme(self.config_manager.get("theme", "dark"))
            if new_theme != self.style_manager.theme:
                self.style_manager.set_theme(new_theme)
                self.apply_theme()
            
            # Update window position if changed
            self.position_window()
            
            # Update display
            self.update_display()
    
    def apply_theme(self):
        """Apply the current theme to all UI elements."""
        self.container.setStyleSheet(self.style_manager.get_style("main_window"))
        self.main_label.setStyleSheet(self.style_manager.get_style("main_label"))
        self.title_label.setStyleSheet(self.style_manager.get_style("title_label"))
        self.debug_btn.setStyleSheet(self.style_manager.get_style("debug_button"))
        self.settings_btn.setStyleSheet(self.style_manager.get_style("settings_button"))
        self.close_btn.setStyleSheet(self.style_manager.get_style("close_button"))
        self.progress_bar.setStyleSheet(self.style_manager.get_style("progress_bar"))
        
        # Update status indicator color
        state, _ = self.break_logic.get_current_state()
        color = self.style_manager.get_status_color(state.value)
        self.status_indicator.update_status(state, color)
    
    def mousePressEvent(self, event):
        """Handle mouse press events for dragging."""
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_start_position = event.globalPos() - self.frameGeometry().topLeft()
            self.setCursor(Qt.ClosedHandCursor)
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move events for dragging."""
        if event.buttons() == Qt.LeftButton and self.dragging:
            self.move(event.globalPos() - self.drag_start_position)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release events to stop dragging."""
        if event.button() == Qt.LeftButton:
            self.dragging = False
            self.setCursor(Qt.OpenHandCursor)
            event.accept()
    
    def enterEvent(self, event):
        """Handle mouse enter events for hover effects."""
        self.container.setStyleSheet(self.style_manager.get_style("main_window_hover"))
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Handle mouse leave events to restore normal appearance."""
        self.container.setStyleSheet(self.style_manager.get_style("main_window"))
        super().leaveEvent(event)
    
    def contextMenuEvent(self, event):
        """Handle right-click context menu."""
        menu = QtWidgets.QMenu(self)
        
        # Settings action
        settings_action = menu.addAction("⚙️ Settings")
        settings_action.triggered.connect(self.open_settings)
        
        # Theme submenu
        theme_menu = menu.addMenu("🎨 Theme")
        
        dark_action = theme_menu.addAction("🌙 Dark")
        dark_action.setCheckable(True)
        dark_action.setChecked(self.style_manager.theme == Theme.DARK)
        dark_action.triggered.connect(lambda: self.change_theme(Theme.DARK))
        
        light_action = theme_menu.addAction("☀️ Light")
        light_action.setCheckable(True)
        light_action.setChecked(self.style_manager.theme == Theme.LIGHT)
        light_action.triggered.connect(lambda: self.change_theme(Theme.LIGHT))
        
        menu.addSeparator()
        
        # About action
        about_action = menu.addAction("ℹ️ About")
        about_action.triggered.connect(self.show_about)
        
        # Close action
        close_action = menu.addAction("❌ Close")
        close_action.triggered.connect(self.close)
        
        menu.exec_(event.globalPos())
    
    def change_theme(self, theme: Theme):
        """Change the application theme.
        
        Args:
            theme: New theme to apply
        """
        self.style_manager.set_theme(theme)
        self.config_manager.set("theme", theme.value)
        self.config_manager.save()
        self.apply_theme()
    
    def show_about(self):
        """Show about dialog."""
        from .. import __version__, __description__
        
        msg = QtWidgets.QMessageBox(self)
        msg.setWindowTitle("About Break Reminder")
        msg.setText(f"""
        <h3>Break Reminder</h3>
        <p>Version: {__version__}</p>
        <p>{__description__}</p>
        <p>Built with PyQt5 for better work-life balance.</p>
        """)
        msg.setStyleSheet(self.style_manager.get_style("dialog_base"))
        msg.exec_()
    
    def closeEvent(self, event):
        """Handle window close event."""
        # Save window position
        # (Could be implemented if needed)
        event.accept()