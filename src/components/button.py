from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt

class ATMButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setMinimumHeight(50)
        self.setCursor(Qt.PointingHandCursor)