import sys
from PyQt6.QtCore import QTimer, Qt, QRect
from PyQt6.QtGui import QPainter, QColor, QBrush, QFont
from PyQt6.QtWidgets import QApplication, QWidget, QInputDialog
import sqlite3
import datetime
class database1:
    def __init__(self):
        self.conn = sqlite3.connect('CozyNights.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS LateNightNotes (notes TEXT,TimeAdded TEXT DEFAULT CURRENT_TIMESTAMP,Feeling TEXT)")
    def add_note(self,notes ,feeling):
        self.cursor.execute("INSERT INTO LateNightNotes VALUES(?,datetime('now','localtime'),?)",(notes,feeling))
        self.conn.commit()
    def get_notes(self):
        self.cursor.execute("SELECT notes,feeling FROM LateNightNotes ORDER BY TimeAdded DESC LIMIT 1")
        x = self.cursor.fetchone()
        return x
class CozySleepApp(QWidget):
    def __init__(self):
        super().__init__()
        self.db = database1()
        self.current_time_str = ""
        self.sky_color = QColor("#0d1b2a")
        self.celestial_look = QColor("#fdf0d5")
        self.clock_text_color = QColor("white")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.initUI()
        self.update_time()
    def initUI(self):
        self.setWindowTitle("CozySleep")
        self.setGeometry(200, 100, 800, 600)
    def update_time(self):
        now = datetime.datetime.now()
        self.current_time_str = now.strftime("%H:%M:%S")
        hour = now.hour
        if 6 <= hour <= 18:
            self.sky_color = QColor("#8ecae6")
            self.celestial_look = QColor("#ffb703")
            self.clock_text_color = QColor("#023047")
        else:
            self.sky_color = QColor("#0d1b2a")
            self.celestial_look = QColor("#fdf0d5")
            self.clock_text_color = QColor("white")
        self.update()
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), self.sky_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(self.celestial_look))
        painter.drawEllipse(650, 60, 80, 80)
        latest_note = self.db.get_notes()
        if latest_note:
            note_text , feeling_text = latest_note
            painter.setBrush(QColor("#f4f1de"))
            painter.drawRect(50,150,220,300)
            painter.fillRect(50,150,220,12,QColor("#e07a5f"))
            painter.setPen(QColor("#2b2b2b"))
            painter.setFont(QFont("Verdana", 10, QFont.Weight.Normal))
            text_box = QRect(60,180,200,220)
            painter.drawText(text_box, Qt.AlignmentFlag.AlignLeft | Qt.TextFlag.TextWordWrap, f"“{note_text}”")
            painter.setFont(QFont("Verdana", 9, QFont.Weight.Bold))
            painter.drawText(60, 430, f"Vibe: {feeling_text}")
        painter.setPen(QColor(self.clock_text_color))
        font = QFont("Verdana", 36, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.current_time_str)
        footer_color = QColor("#023047") if 6 <= datetime.datetime.now().hour < 18 else QColor("#8ecae6")
        painter.setPen(footer_color)
        painter.setFont(QFont("Verdana", 11, QFont.Weight.Normal))
        instruction_box = self.rect().adjusted(0, 240, 0, 0)
        painter.drawText(instruction_box, Qt.AlignmentFlag.AlignCenter, "Press [N] to log a note")
# press N on Your Keyboard for adding notes
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_N:
            self.take_note()
    def take_note(self):
        note_text, ok1 = QInputDialog.getText(self,"late night note","Whats in ur mind?")
        if ok1 and note_text:
            feeling_text,ok2 = QInputDialog.getText(self,"Current Mood?","How Are u feeling rn?")
            if ok2 and feeling_text:
                self.db.add_note(note_text,feeling_text)
                self.update()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CozySleepApp()
    window.show()
    sys.exit(app.exec())
