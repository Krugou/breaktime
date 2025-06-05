
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
        self.label = QtWidgets.QLabel('', self)
        self.label.setStyleSheet('background: rgba(30,30,30,200); color: white; font-size: 16px; padding: 10px; border-radius: 8px;')
        layout = QtWidgets.QVBoxLayout()
        # Debug toggle and close button row
        top_row = QtWidgets.QHBoxLayout()
        self.debug_btn = QtWidgets.QPushButton('🐞')
        self.debug_btn.setFixedSize(20, 20)
        self.debug_btn.setStyleSheet('background: #444; color: yellow; border: none; border-radius: 10px; font-size: 14px;')
        self.debug_btn.setToolTip('Toggle debug info')
        self.debug_btn.setCheckable(True)
        self.debug_btn.toggled.connect(self.toggle_debug)
        self.close_btn = QtWidgets.QPushButton('×')
        self.close_btn.setFixedSize(20, 20)
        self.close_btn.setStyleSheet('background: #a00; color: white; border: none; border-radius: 10px; font-weight: bold; font-size: 14px;')
        self.close_btn.clicked.connect(self.close)
        top_row.addWidget(self.debug_btn)
        top_row.addStretch()
        top_row.addWidget(self.close_btn)
        layout.addLayout(top_row)
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.resize(260, 80)
        self.move_to_top_right()

    def toggle_debug(self, checked):
        self.debug_enabled = checked
        self.update_reminder()

    def move_to_top_right(self):
        screen = QtWidgets.QApplication.primaryScreen().geometry()
        self.move(screen.width() - self.width() - 20, 20)

    def update_reminder(self):
        now = datetime.now()
        debug_lines = []
        # If workday is over
        if now >= self.workday_end:
            label = random.choice(self.FINNISH_FUNNY_MESSAGES)
            if self.debug_enabled:
                debug_lines.append(f"Now: {now.strftime('%Y-%m-%d %H:%M:%S')}")
                debug_lines.append(f"Workday end: {self.workday_end.strftime('%Y-%m-%d %H:%M:%S')}")
                debug_lines.append(f"Start: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
                debug_lines.append(f"Lunch: {self.lunch_start.strftime('%H:%M')} - {self.lunch_end.strftime('%H:%M')}")
            self.label.setText(label + ("\n" + "\n".join(debug_lines) if debug_lines else ""))
            if not self.close_timer_started:
                self.close_timer_started = True
                QtCore.QTimer.singleShot(30 * 60 * 1000, self.close)  # autoclose after 30 min
            return
        # Lunch break window
        if self.lunch_start <= now <= self.lunch_end:
            mins_left = int((self.lunch_end - now).total_seconds() // 60)
            mins_since = int((now - self.lunch_start).total_seconds() // 60)
            if mins_since < 0:
                mins_since = 0
            label = f"Lunch break! ({mins_left} min left)"
            if self.debug_enabled:
                debug_lines.append(f"Now: {now.strftime('%Y-%m-%d %H:%M:%S')}")
                debug_lines.append(f"Lunch: {self.lunch_start.strftime('%H:%M')} - {self.lunch_end.strftime('%H:%M')}")
            self.label.setText(label + ("\n" + "\n".join(debug_lines) if debug_lines else ""))
        else:
            # Normal breaks
            while self.next_break_idx < len(self.break_times) and now > self.break_times[self.next_break_idx]:
                self.next_break_idx += 1
            if self.next_break_idx < len(self.break_times):
                next_break = self.break_times[self.next_break_idx]
                mins_left = int((next_break - now).total_seconds() // 60)
                label = f"Next break: {next_break.strftime('%H:%M')} ({mins_left} min left)"
            else:
                # add time until workday end
                mins_left = int((self.workday_end - now).total_seconds() // 60)
                label = f"No more breaks today! ({mins_left} min left)"
            if self.debug_enabled:
                debug_lines.append(f"Now: {now.strftime('%Y-%m-%d %H:%M:%S')}")
                debug_lines.append(f"Start: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
                debug_lines.append(f"Next break: {self.break_times[self.next_break_idx].strftime('%Y-%m-%d %H:%M:%S') if self.next_break_idx < len(self.break_times) else 'N/A'}")
                debug_lines.append(f"Workday end: {self.workday_end.strftime('%Y-%m-%d %H:%M:%S')}")
                debug_lines.append(f"Lunch: {self.lunch_start.strftime('%H:%M')} - {self.lunch_end.strftime('%H:%M')}")
            self.label.setText(label + ("\n" + "\n".join(debug_lines) if debug_lines else ""))




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
    dialog.setWindowTitle("Set Work and Lunch Times")

    layout = QtWidgets.QFormLayout(dialog)

    start_edit = QtWidgets.QLineEdit(config["usual_start"])
    lunch_start_edit = QtWidgets.QLineEdit(config["lunch_start"])
    lunch_end_edit = QtWidgets.QLineEdit(config["lunch_end"])
    workday_length_edit = QtWidgets.QLineEdit(config.get("workday_length", "08:00"))

    layout.addRow("Start time (HH:MM):", start_edit)
    layout.addRow("Lunch start (HH:MM):", lunch_start_edit)
    layout.addRow("Lunch end (HH:MM):", lunch_end_edit)
    layout.addRow("Workday length (HH:MM):", workday_length_edit)

    btns = QtWidgets.QDialogButtonBox()
    usual_btn = QtWidgets.QPushButton("Usual Start")
    btns.addButton(usual_btn, QtWidgets.QDialogButtonBox.ActionRole)
    btns.setStandardButtons(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
    layout.addRow(btns)

    def set_usual():
        start_edit.setText(config["usual_start"])
        lunch_start_edit.setText(config["lunch_start"])
        lunch_end_edit.setText(config["lunch_end"])
        workday_length_edit.setText(config.get("workday_length", "08:00"))
    usual_btn.clicked.connect(set_usual)

    result = btns.exec_ if hasattr(btns, 'exec_') else dialog.exec_
    def accept():
        dialog.accept()
    def reject():
        dialog.reject()
    btns.accepted.connect(accept)
    btns.rejected.connect(reject)

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
    msg.setWindowTitle("Start Work")
    msg.setText(f"Start with usual times?\nStart: {config['usual_start']}\nLunch: {config['lunch_start']} - {config['lunch_end']}")
    usual_btn = msg.addButton("Usual", QtWidgets.QMessageBox.AcceptRole)
    edit_btn = msg.addButton("Edit", QtWidgets.QMessageBox.ActionRole)
    cancel_btn = msg.addButton("Cancel", QtWidgets.QMessageBox.RejectRole)
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
