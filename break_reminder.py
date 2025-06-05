import sys
from PyQt5 import QtWidgets, QtCore
from datetime import datetime, timedelta

class BreakReminder(QtWidgets.QWidget):
    def __init__(self, start_time):
        super().__init__()
        self.start_time = start_time
        self.break_points = [0.25, 1.0]  # 1/4 and end of day
        self.total_hours = 8
        self.break_times = [self.start_time + timedelta(hours=self.total_hours * p) for p in self.break_points]
        # Lunch break window: 10:45 to 12:30
        today = self.start_time.date()
        self.lunch_start = datetime.combine(today, datetime.strptime('10:45', '%H:%M').time())
        self.lunch_end = datetime.combine(today, datetime.strptime('12:30', '%H:%M').time())
        self.next_break_idx = 0
        self.workday_end = self.start_time + timedelta(hours=self.total_hours)
        self.close_timer_started = False
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
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.resize(260, 60)
        self.move_to_top_right()

    def move_to_top_right(self):
        screen = QtWidgets.QApplication.primaryScreen().geometry()
        self.move(screen.width() - self.width() - 20, 20)

    def update_reminder(self):
        now = datetime.now()
        # If workday is over
        if now >= self.workday_end:
            label = "Workday complete!"
            self.label.setText(label)
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
        else:
            # Normal breaks
            while self.next_break_idx < len(self.break_times) and now > self.break_times[self.next_break_idx]:
                self.next_break_idx += 1
            if self.next_break_idx < len(self.break_times):
                next_break = self.break_times[self.next_break_idx]
                mins_left = int((next_break - now).total_seconds() // 60)
                if self.next_break_idx == 0:
                    label = f"Next break: {next_break.strftime('%H:%M')} ({mins_left} min left)"
                else:
                    label = "Workday complete!"
            else:
                label = "Workday complete!"
        self.label.setText(label)


def get_start_time():
    text, ok = QtWidgets.QInputDialog.getText(None, 'Start Time', 'Enter start time (HH:MM):')
    if ok:
        try:
            today = datetime.now().date()
            t = datetime.strptime(text, '%H:%M').time()
            return datetime.combine(today, t)
        except Exception:
            QtWidgets.QMessageBox.warning(None, 'Invalid', 'Please enter time as HH:MM')
            return get_start_time()
    else:
        sys.exit()


def main():
    app = QtWidgets.QApplication(sys.argv)
    start_time = get_start_time()
    reminder = BreakReminder(start_time)
    reminder.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
