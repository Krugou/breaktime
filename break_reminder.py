import sys
import random
from PyQt5 import QtWidgets, QtCore
from datetime import datetime, timedelta
import json
import os

class BreakReminder(QtWidgets.QWidget):
    FINNISH_FUNNY_MESSAGES = [
        "Työpäivä ohi! Nyt kahville!",
        "Valmista tuli, mene vaikka ulos haukkaamaan happea!",
        "Työt tehty, nyt voi ottaa rennosti!",
        "Nyt on aika sulkea läppäri ja avata elämä!",
        "Työpäivä paketissa – ansaittu tauko!",
        "Voit vihdoin lakata teeskentelemästä kiireistä!",
        "Nyt on lupa olla tekemättä mitään!",
        "Työpäivä ohi, muista venytellä!",
        "Nyt vaikka saunaan!",
        "Hyvää työtä, nyt huilaamaan!"
    ]
    def __init__(self, start_time):
        super().__init__()
        self.start_time = start_time
        self.break_points = [0.25, 0.75]  # 1/4 and 3/4 of the workday
        self.total_hours = 8
        self.break_times = [self.start_time + timedelta(hours=self.total_hours * p) for p in self.break_points]
        # Lunch break window: 10:45 to 12:30
        today = self.start_time.date()
        self.lunch_start = datetime.combine(today, datetime.strptime('10:45', '%H:%M').time())
        self.lunch_end = datetime.combine(today, datetime.strptime('12:30', '%H:%M').time())
        self.next_break_idx = 0
        self.workday_end = self.start_time + timedelta(hours=self.total_hours)
        self.close_timer_started = False
        self.debug_enabled = False

        # Variables for drag functionality
        self.dragging = False
        self.drag_start_position = None

        self.initUI()
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update_reminder)
        self.update_timer.start(1000 * 60)  # check every minute
        self.update_reminder()

    def initUI(self):
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.Tool
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
          # Main container widget
        self.container = QtWidgets.QWidget()
        self.container.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(45, 45, 55, 240),
                    stop:1 rgba(25, 25, 35, 240));
                border-radius: 12px;
                border: 2px solid rgba(100, 100, 120, 80);
            }
        """)
        self.container.setCursor(QtCore.Qt.OpenHandCursor)

        # Status indicator
        self.status_indicator = QtWidgets.QLabel('●')
        self.status_indicator.setAlignment(QtCore.Qt.AlignCenter)
        self.status_indicator.setFixedSize(12, 12)
        self.update_status_indicator('work')

        # Main label with improved styling
        self.label = QtWidgets.QLabel('', self)
        self.label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: 500;
                font-family: 'Segoe UI', Arial, sans-serif;
                padding: 12px 16px;
                background: transparent;
                border: none;
                line-height: 1.4;
            }
        """)
        self.label.setWordWrap(True)

        # Create main layout
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header row with status, title and controls
        header_row = QtWidgets.QHBoxLayout()
        header_row.setContentsMargins(12, 8, 12, 0)
        header_row.setSpacing(8)

        # Status and title section
        status_section = QtWidgets.QHBoxLayout()
        status_section.setSpacing(8)
        status_section.addWidget(self.status_indicator)

        title_label = QtWidgets.QLabel("Break Reminder")
        title_label.setStyleSheet("""
            color: rgba(255, 255, 255, 180);
            font-size: 11px;
            font-weight: 600;
            background: transparent;
            border: none;
        """)
        status_section.addWidget(title_label)
        status_section.addStretch()

        header_row.addLayout(status_section)

        # Control buttons
        controls_layout = QtWidgets.QHBoxLayout()
        controls_layout.setSpacing(4)

        self.debug_btn = QtWidgets.QPushButton('🐞')
        self.debug_btn.setFixedSize(28, 28)
        self.debug_btn.setStyleSheet("""
            QPushButton {
                background: rgba(80, 80, 90, 150);
                color: #FFE066;
                border: 1px solid rgba(100, 100, 110, 100);
                border-radius: 14px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(100, 100, 110, 180);
                border: 1px solid rgba(120, 120, 130, 150);
            }
            QPushButton:pressed {
                background: rgba(60, 60, 70, 200);
            }
            QPushButton:checked {
                background: rgba(255, 224, 102, 200);
                color: #333;
            }
        """)
        self.debug_btn.setToolTip('Toggle debug info')
        self.debug_btn.setCheckable(True)
        self.debug_btn.toggled.connect(self.toggle_debug)

        self.close_btn = QtWidgets.QPushButton('×')
        self.close_btn.setFixedSize(28, 28)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background: rgba(180, 50, 50, 150);
                color: white;
                border: 1px solid rgba(200, 70, 70, 100);
                border-radius: 14px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background: rgba(200, 70, 70, 180);
                border: 1px solid rgba(220, 90, 90, 150);
            }
            QPushButton:pressed {
                background: rgba(160, 30, 30, 200);
            }
        """)
        self.close_btn.clicked.connect(self.close)

        controls_layout.addWidget(self.debug_btn)
        controls_layout.addWidget(self.close_btn)
        header_row.addLayout(controls_layout)

        # Add components to main layout
        layout.addLayout(header_row)
        layout.addWidget(self.label)

        self.container.setLayout(layout)
          # Main widget layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(6, 6, 6, 6)
        main_layout.addWidget(self.container)
        self.setLayout(main_layout)

        self.resize(320, 120)
        self.move_to_top_right()
        self.add_drop_shadow()

        # Set tooltip for drag functionality
        self.setToolTip("💡 Click and drag to move this window anywhere on your screen")

    def toggle_debug(self, checked):
        self.debug_enabled = checked
        self.update_reminder()

    def move_to_top_right(self):
        screen = QtWidgets.QApplication.primaryScreen().geometry()
        self.move(screen.width() - self.width() - 20, 20)

    def update_reminder(self):
        now = datetime.now()
        debug_lines = []        # If workday is over
        if now >= self.workday_end:
            label = f"🎉 {random.choice(self.FINNISH_FUNNY_MESSAGES)}"
            if self.debug_enabled:
                debug_lines.append(f"📅 Now: {now.strftime('%Y-%m-%d %H:%M:%S')}")
                debug_lines.append(f"🏁 Workday end: {self.workday_end.strftime('%Y-%m-%d %H:%M:%S')}")
                debug_lines.append(f"🚀 Start: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
                debug_lines.append(f"🍽️ Lunch: {self.lunch_start.strftime('%H:%M')} - {self.lunch_end.strftime('%H:%M')}")
            self.label.setText(label + ("\n\n" + "\n".join(debug_lines) if debug_lines else ""))
            self.update_status_indicator('done')
            if not self.close_timer_started:
                self.close_timer_started = True
                QtCore.QTimer.singleShot(30 * 60 * 1000, self.close)  # autoclose after 30 min
            return        # Lunch break window
        if self.lunch_start <= now <= self.lunch_end:
            mins_left = int((self.lunch_end - now).total_seconds() // 60)
            mins_since = int((now - self.lunch_start).total_seconds() // 60)
            if mins_since < 0:
                mins_since = 0
            label = f"🍽️ Lunch break!\n⏰ {mins_left} minutes left"
            if self.debug_enabled:
                debug_lines.append(f"📅 Now: {now.strftime('%Y-%m-%d %H:%M:%S')}")
                debug_lines.append(f"🍽️ Lunch: {self.lunch_start.strftime('%H:%M')} - {self.lunch_end.strftime('%H:%M')}")
            self.label.setText(label + ("\n\n" + "\n".join(debug_lines) if debug_lines else ""))
            self.update_status_indicator('lunch')
        else:
            # Normal breaks
            while self.next_break_idx < len(self.break_times) and now > self.break_times[self.next_break_idx]:
                self.next_break_idx += 1
            if self.next_break_idx < len(self.break_times):
                next_break = self.break_times[self.next_break_idx]
                mins_left = int((next_break - now).total_seconds() // 60)

                # Check if we're at break time (within 5 minutes)
                if mins_left <= 5 and mins_left >= 0:
                    label = f"☕ Break time!\n⏰ {next_break.strftime('%H:%M')} ({mins_left} min)"
                    self.update_status_indicator('break')
                else:
                    label = f"💼 Next break: {next_break.strftime('%H:%M')}\n⏰ {mins_left} minutes to go"
                    self.update_status_indicator('work')
            else:
                # No more breaks, show time until workday end
                mins_left = int((self.workday_end - now).total_seconds() // 60)
                hours_left = mins_left // 60
                mins_remaining = mins_left % 60
                if hours_left > 0:
                    time_str = f"{hours_left}h {mins_remaining}m"
                else:
                    time_str = f"{mins_remaining}m"
                label = f"🏁 No more breaks today!\n⏰ {time_str} until home time"
                self.update_status_indicator('work')
            if self.debug_enabled:
                debug_lines.append(f"📅 Now: {now.strftime('%Y-%m-%d %H:%M:%S')}")
                debug_lines.append(f"🚀 Start: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
                debug_lines.append(f"☕ Next break: {self.break_times[self.next_break_idx].strftime('%Y-%m-%d %H:%M:%S') if self.next_break_idx < len(self.break_times) else 'N/A'}")
                debug_lines.append(f"🏁 Workday end: {self.workday_end.strftime('%Y-%m-%d %H:%M:%S')}")
                debug_lines.append(f"🍽️ Lunch: {self.lunch_start.strftime('%H:%M')} - {self.lunch_end.strftime('%H:%M')}")
            self.label.setText(label + ("\n\n" + "\n".join(debug_lines) if debug_lines else ""))

    def update_status_indicator(self, state):
        """Update the status indicator color based on current state"""
        colors = {
            'work': '#4CAF50',      # Green for work time
            'break': '#FF9800',     # Orange for break time
            'lunch': '#2196F3',     # Blue for lunch time
            'done': '#9C27B0'       # Purple for workday done
        }
        color = colors.get(state, '#4CAF50')
        self.status_indicator.setStyleSheet(f"""
            color: {color};
            font-size: 20px;
            background: transparent;
            border: none;
        """)

    def add_drop_shadow(self):
        """Add a subtle drop shadow effect to the widget"""
        try:
            # This will only work on Windows, but we'll handle gracefully if not available
            from PyQt5.QtWidgets import QGraphicsDropShadowEffect
            from PyQt5.QtCore import QPointF
            from PyQt5.QtGui import QColor

            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(20)
            shadow.setColor(QColor(0, 0, 0, 60))
            shadow.setOffset(QPointF(0, 4))
            self.container.setGraphicsEffect(shadow)
        except:
            # If shadow effect is not available, continue without it
            pass

    def mousePressEvent(self, event):
        """Handle mouse press events for drag functionality"""
        if event.button() == QtCore.Qt.LeftButton:
            self.dragging = True
            self.drag_start_position = event.globalPos() - self.frameGeometry().topLeft()
            self.setCursor(QtCore.Qt.ClosedHandCursor)
            event.accept()

    def mouseMoveEvent(self, event):
        """Handle mouse move events for dragging"""
        if event.buttons() == QtCore.Qt.LeftButton and self.dragging:
            self.move(event.globalPos() - self.drag_start_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        """Handle mouse release events to stop dragging"""
        if event.button() == QtCore.Qt.LeftButton:
            self.dragging = False
            self.setCursor(QtCore.Qt.OpenHandCursor)
            event.accept()

    def enterEvent(self, event):
        """Show visual feedback when mouse enters the widget"""
        self.container.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(55, 55, 65, 250),
                    stop:1 rgba(35, 35, 45, 250));
                border-radius: 12px;
                border: 2px solid rgba(120, 120, 140, 120);
            }
        """)

    def leaveEvent(self, event):
        """Restore normal appearance when mouse leaves the widget"""
        self.container.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(45, 45, 55, 240),
                    stop:1 rgba(25, 25, 35, 240));
                border-radius: 12px;
                border: 2px solid rgba(100, 100, 120, 80);
            }
        """)




# Config file for storing usual start, lunch times, and workday length
CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".break_reminder_config.json")

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    # Defaults
    return {
        "usual_start": "08:00",
        "lunch_start": "10:45",
        "lunch_end": "12:30",
        "workday_length": "08:00"  # hours:minutes
    }

def save_config(config):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
    except Exception:
        pass

def get_times_dialog():
    config = load_config()
    dialog = QtWidgets.QDialog()
    dialog.setWindowTitle("⚙️ Configure Work Schedule")
    dialog.setFixedSize(400, 280)
    dialog.setStyleSheet("""
        QDialog {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #f8f9fa, stop:1 #e9ecef);
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        QLabel {
            color: #495057;
            font-weight: 500;
            font-size: 14px;
            margin: 4px 0;
        }
        QLineEdit {
            border: 2px solid #dee2e6;
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 14px;
            background: white;
            selection-background-color: #007bff;
        }
        QLineEdit:focus {
            border-color: #007bff;
            outline: none;
        }
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #007bff, stop:1 #0056b3);
            border: none;
            color: white;
            padding: 10px 20px;
            border-radius: 6px;
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
        QPushButton[text="Usual Start"] {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #28a745, stop:1 #1e7e34);
        }
        QPushButton[text="Usual Start"]:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #1e7e34, stop:1 #155724);
        }
    """)

    layout = QtWidgets.QVBoxLayout(dialog)
    layout.setSpacing(16)
    layout.setContentsMargins(24, 24, 24, 24)

    # Title
    title = QtWidgets.QLabel("Configure your work schedule")
    title.setStyleSheet("font-size: 18px; font-weight: bold; color: #212529; margin-bottom: 8px;")
    layout.addWidget(title)

    # Form layout
    form_layout = QtWidgets.QFormLayout()
    form_layout.setSpacing(12)
    form_layout.setVerticalSpacing(8)

    start_edit = QtWidgets.QLineEdit(config["usual_start"])
    start_edit.setPlaceholderText("e.g., 08:00")

    lunch_start_edit = QtWidgets.QLineEdit(config["lunch_start"])
    lunch_start_edit.setPlaceholderText("e.g., 11:00")

    lunch_end_edit = QtWidgets.QLineEdit(config["lunch_end"])
    lunch_end_edit.setPlaceholderText("e.g., 12:00")

    workday_length_edit = QtWidgets.QLineEdit(config.get("workday_length", "08:00"))
    workday_length_edit.setPlaceholderText("e.g., 08:00")

    form_layout.addRow("🚀 Start time (HH:MM):", start_edit)
    form_layout.addRow("🍽️ Lunch start (HH:MM):", lunch_start_edit)
    form_layout.addRow("🍽️ Lunch end (HH:MM):", lunch_end_edit)
    form_layout.addRow("⏰ Workday length (HH:MM):", workday_length_edit)

    layout.addLayout(form_layout)

    # Buttons
    btns_layout = QtWidgets.QHBoxLayout()
    btns_layout.setSpacing(12)

    usual_btn = QtWidgets.QPushButton("Usual Start")
    cancel_btn = QtWidgets.QPushButton("Cancel")
    ok_btn = QtWidgets.QPushButton("OK")

    def set_usual():
        start_edit.setText(config["usual_start"])
        lunch_start_edit.setText(config["lunch_start"])
        lunch_end_edit.setText(config["lunch_end"])
        workday_length_edit.setText(config.get("workday_length", "08:00"))
    usual_btn.clicked.connect(set_usual)

    def accept():
        dialog.accept()
    def reject():
        dialog.reject()
    ok_btn.clicked.connect(accept)
    cancel_btn.clicked.connect(reject)

    btns_layout.addWidget(usual_btn)
    btns_layout.addStretch()
    btns_layout.addWidget(cancel_btn)
    btns_layout.addWidget(ok_btn)
    layout.addLayout(btns_layout)

    if dialog.exec_() == QtWidgets.QDialog.Accepted:
        start = start_edit.text()
        lunch_start = lunch_start_edit.text()
        lunch_end = lunch_end_edit.text()
        workday_length = workday_length_edit.text()
        # Save as new usual
        config["usual_start"] = start
        config["lunch_start"] = lunch_start
        config["lunch_end"] = lunch_end
        config["workday_length"] = workday_length
        save_config(config)
        return start, lunch_start, lunch_end, workday_length
    else:
        sys.exit()

def get_start_and_lunch_times():
    # Ask if user wants to use usual or edit
    config = load_config()
    msg = QtWidgets.QMessageBox()
    msg.setWindowTitle("🌅 Start Your Workday")
    msg.setStyleSheet("""
        QMessageBox {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #f8f9fa, stop:1 #e9ecef);
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        QMessageBox QLabel {
            color: #495057;
            font-size: 14px;
            font-weight: 500;
        }
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #007bff, stop:1 #0056b3);
            border: none;
            color: white;
            padding: 8px 16px;
            border-radius: 5px;
            font-weight: 600;
            font-size: 13px;
            min-width: 70px;
        }
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #0056b3, stop:1 #004085);
        }
    """)
    msg.setText(f"Ready to start working? 💼\n\n🕒 Start: {config['usual_start']}\n🍽️ Lunch: {config['lunch_start']} - {config['lunch_end']}\n⏰ Length: {config.get('workday_length', '08:00')}")
    usual_btn = msg.addButton("✅ Use Usual", QtWidgets.QMessageBox.AcceptRole)
    edit_btn = msg.addButton("⚙️ Edit Times", QtWidgets.QMessageBox.ActionRole)
    cancel_btn = msg.addButton("❌ Cancel", QtWidgets.QMessageBox.RejectRole)
    msg.exec_()
    if msg.clickedButton() == usual_btn:
        return config["usual_start"], config["lunch_start"], config["lunch_end"], config.get("workday_length", "08:00")
    elif msg.clickedButton() == edit_btn:
        return get_times_dialog()
    else:
        sys.exit()


def main():
    app = QtWidgets.QApplication(sys.argv)
    start_str, lunch_start_str, lunch_end_str, workday_length_str = get_start_and_lunch_times()
    today = datetime.now().date()
    try:
        start_time = datetime.combine(today, datetime.strptime(start_str, '%H:%M').time())
        lunch_start = datetime.combine(today, datetime.strptime(lunch_start_str, '%H:%M').time())
        lunch_end = datetime.combine(today, datetime.strptime(lunch_end_str, '%H:%M').time())
        # Parse workday length
        wh, wm = [int(x) for x in workday_length_str.split(":")] if ":" in workday_length_str else (int(workday_length_str), 0)
        workday_length = timedelta(hours=wh, minutes=wm)
    except Exception:
        QtWidgets.QMessageBox.warning(None, 'Invalid', 'Please enter time as HH:MM')
        sys.exit()
    # Patch BreakReminder to use custom lunch times and workday length
    class CustomBreakReminder(BreakReminder):
        def __init__(self, start_time):
            super().__init__(start_time)
            self.lunch_start = lunch_start
            self.lunch_end = lunch_end
            self.total_hours = workday_length.total_seconds() / 3600
            self.break_times = [self.start_time + timedelta(hours=self.total_hours * p) for p in self.break_points]
            self.workday_end = self.start_time + workday_length
    reminder = CustomBreakReminder(start_time)
    reminder.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
