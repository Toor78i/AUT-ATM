from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from components.button import ATMButton
from utils.animations import fade_in

class ErrorDialog(QDialog):
    def __init__(self, message):
        super().__init__()
        self.setWindowTitle("Error")
        self.setFixedWidth(300)
        self.setModal(True)
        self.setup_ui(message)

    def setup_ui(self, message):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        label = QLabel(message)
        label.setObjectName("label")
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        ok_button = ATMButton("OK")
        ok_button.setMinimumWidth(100)
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def showEvent(self, event):
        super().showEvent(event)
        fade_in(self)