import sqlite3
import sys
import random
from PyQt6.QtCore import Qt,QTimer,QRect
from PyQt6.QtGui import QPainter, QColor, QFont
from PyQt6.QtWidgets import QApplication, QWidget, QLabel,QInputDialog
import datetime
class DataBase1:
    def __init__(self):
        self.sql = sqlite3.connect('learninggui.db')
        self.cursor = self.sql.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS NotesTable(notes TEXT, time_added DATETIME DEFAULT CURRENT_TIMESTAMP)")
        self.sql.commit()
    def add_notes(self,notesadded):
        self.cursor.execute("INSERT INTO NotesTable(notes) VALUES(?)",(notesadded,))
        self.sql.commit()
    def get_notes(self):
        self.cursor.execute("SELECT notes FROM NotesTable")
        x = self.cursor.fetchall()
        return x
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DataBase1()
        self.moon_y = 0
        self.sun_y = 795
        self.is_daytime = False
        self.stars = []
        for _ in range(1000):
            x = random.randint(1,1530)
            y = random.randint(1,790)
            brightness = random.randint(50,255)
            self.stars.append([x,y,brightness])
        self.setWindowTitle("Fucking PyQt6.QtGui")
        self.setGeometry(3,40,1530,760)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.label = QLabel(self)
        self.update_time()
        self.styling()
    def styling(self):
        self.label.setGeometry(723,130,700,550)
        self.setStyleSheet("""QLabel {font-size: 23px;
                                    font-weight: bold;
                                    font-family: Verdana;
                                    color: white;}""")
    def paintEvent(self,event):
        painter = QPainter(self)

        if not self.is_daytime:
            painter.fillRect(self.rect(), QColor("#0d1b2a"))
            painter.setPen(Qt.PenStyle.NoPen)
            for x,y,brightness in self.stars:
                painter.setBrush(QColor(255,255,255,brightness))
                painter.drawEllipse(x,y,2,2)
        else:
            painter.fillRect(self.rect(), QColor("#4a90e2"))
        painter.setBrush(QColor("#F6F1D5"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, self.moon_y, 100, 100)
        painter.setBrush(QColor("#ffde4d"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, self.sun_y, 100, 100)
        painter.setBrush(QColor("#fff275"))
        painter.drawRect(450, 100, 240, 400)
        painter.setBrush(QColor("#644B00"))
        painter.drawRect(450, 100, 240, 30)
        row = self.db.get_notes()
        notes = [note[0] for note in row]
        sticky_text = "\n".join(notes)
        painter.setPen(QColor("#333333"))
        painter.setFont(QFont("Verdana", 12, QFont.Weight.Bold))
        text_rect = QRect(460, 140, 220, 340)
        flags = int(Qt.AlignmentFlag.AlignLeft) | int(Qt.TextFlag.TextWordWrap)
        painter.drawText(text_rect, flags, sticky_text)
    def update_time(self):
        now = datetime.datetime.now()
        self.label.setText(now.strftime("%H:%M:%S"))

        if not self.is_daytime:
            if self.moon_y < 795:
                self.moon_y += 15
            else:
                self.is_daytime = True

        else:
            if self.sun_y > 0:
                self.sun_y -=15
            else:
                self.moon_y = 0
                self.sun_y = 795
                self.is_daytime = False
        for star in self.stars:
            star[2] += random.randint(-50,50)
            star[2] = max(50,min(255,star[2]))
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_N:
            dialog = QInputDialog()
            dialog.setWindowTitle("add notes")
            dialog.setLabelText("type in ur notes")
            dialog.setStyleSheet("""
                    QInputDialog {background-color: #171D20}
                    QLabel {
                    color: white;
                    font-family: Verdana;
                    font-size: 14px;
                }
                QLineEdit {
                    background-color: #1b263b;
                    color: white;
                    border: 2px solid #fff275;
                    border-radius: 4px;
                    padding: 4px;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #fff275;
                    color: #0d1b2a;
                    font-weight: bold;
                    border-radius: 4px;
                    padding: 5px 15px;
                }
                QPushButton:hover {
                    background-color: #e5da69;
                }
             """)
            ok = dialog.exec()
            text = dialog.textValue()
            if ok and text:
                self.db.add_notes(text)
                self.update()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
