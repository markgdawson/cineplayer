from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets
import calendar
from datetime import datetime
import random


class CalendarView(QtWidgets.QWidget):
    def __init__(self, year=2017, month=8, parent=None):
        super(CalendarView, self).__init__(parent)

        self.set_date(year, month)

    def set_date(self, year, month):
        self.buttons = []

        layout = QtWidgets.QGridLayout(self)
        layout.setAlignment(QtCore.Qt.AlignCenter)

        self.month_name = calendar.month_name[month]
        month_label = QtWidgets.QLabel(self.month_name)
        month_label.setAlignment(QtCore.Qt.AlignCenter)
        month_label.setStyleSheet("font-weight: bold; font-size: large")
        layout.addWidget(month_label, 0, 1, 1, 5)

        self.next_button = QtWidgets.QPushButton(self)
        self.next_button.setText("<")
        layout.addWidget(self.next_button, 0, 0, 1, 1)
        self.prev_button = QtWidgets.QPushButton(self)
        self.prev_button.setText(">")
        layout.addWidget(self.prev_button, 0, 6, 1, 1)

        cal = calendar.monthcalendar(year, month)
        for col, weekday in enumerate(['Monday', 'Tueday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']):
            label = QtWidgets.QLabel(self)
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setText(weekday)
            self.layout().addWidget(label, 1, col, 1, 1)

        currday = datetime.now().day
        currmonth = datetime.now().month
        curryear = datetime.now().year

        for row, week in enumerate(cal):
            for col, day in enumerate(week):
                if day > 0:
                    button = QtWidgets.QPushButton(self)
                    film_str = ["Alien", "Jumanji", "Alien\nJumanji", "Finding Nemo\nJumanji\nJaws"][random.randint(0, 3)]
                    button.setText("%d:\n%s" % (day,film_str))
                    button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

                    if day == currday and month == currmonth and year == curryear:
                        button.setStyleSheet("font-weight: bold; font-style: italic;")

                    if datetime(year, month, day).date() < datetime.today().date():
                        button.setEnabled(False)

                    self.layout().addWidget(button, row+2, col, 1, 1)

        self.setLayout(layout)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    a = CalendarView()
    a.show()
    sys.exit(app.exec_())