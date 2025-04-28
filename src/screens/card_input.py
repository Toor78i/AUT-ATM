from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QRegularExpressionValidator
from components.button import ATMButton
from components.error_dialog import ErrorDialog
from utils.animations import fade_in
from PySide6.QtCore import QRegularExpression


class CardInputScreen(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        card = QWidget()
        card.setObjectName("card")
        card_layout = QVBoxLayout()
        card_layout.setAlignment(Qt.AlignCenter)
        card_layout.setSpacing(15)
        card_layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel("Enter Card Number")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)

        self.card_input = QLineEdit()
        self.card_input.setPlaceholderText("1234-1234-1234-1234")
        self.card_input.setMaxLength(19)  # 16 digits + 3 hyphens
        self.card_input.setObjectName("input")
        self.card_input.setAlignment(Qt.AlignCenter)
        self.card_input.setMinimumWidth(350)  # Increased width
        regex = QRegularExpression(r"^\d{0,4}(-?\d{0,4}){0,3}$")
        validator = QRegularExpressionValidator(regex)
        self.card_input.setValidator(validator)
        self.card_input.textChanged.connect(self.format_card_number)
        card_layout.addWidget(self.card_input)

        submit_button = ATMButton("Submit")
        submit_button.clicked.connect(self.on_next)
        card_layout.addWidget(submit_button)

        card.setLayout(card_layout)
        card.setMinimumWidth(500)  # Set minimum width for card
        layout.addWidget(card)
        layout.addStretch()
        self.setLayout(layout)

    def format_card_number(self, text):
        cleaned = "".join(c for c in text if c.isdigit())
        formatted = ""
        for i, char in enumerate(cleaned):
            if i > 0 and i % 4 == 0 and i < 16:
                formatted += "-"
            formatted += char
        self.card_input.blockSignals(True)
        self.card_input.setText(formatted[:19])
        self.card_input.blockSignals(False)

    def on_next(self):
        card_number = "".join(c for c in self.card_input.text() if c.isdigit())
        if len(card_number) == 16:
            self.parent.pin_input_screen.set_card_number(card_number)
            self.parent.switch_screen(self.parent.pin_input_screen)
        else:
            dialog = ErrorDialog("Please enter a valid 16-digit card number")
            dialog.exec()

    def showEvent(self, event):
        super().showEvent(event)
        fade_in(self)
