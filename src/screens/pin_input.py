from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QLineEdit, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator
from components.button import ATMButton
from components.error_dialog import ErrorDialog
from utils.animations import fade_in

class PinInputScreen(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.card_number = ""
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

        title = QLabel("Enter Your PIN")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)

        self.pin_input = QLineEdit()
        self.pin_input.setPlaceholderText("4-digit PIN")
        self.pin_input.setEchoMode(QLineEdit.Password)
        self.pin_input.setMaxLength(4)
        self.pin_input.setMinimumWidth(250)
        self.pin_input.setAlignment(Qt.AlignCenter)
        self.pin_input.setFocusPolicy(Qt.StrongFocus)
        validator = QIntValidator(0, 9999)
        self.pin_input.setValidator(validator)
        card_layout.addWidget(self.pin_input)

        # Numeric keypad
        keypad_layout = QGridLayout()
        keypad_layout.setSpacing(10)
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '', '0', 'Clear']
        for i, num in enumerate(numbers):
            if num:
                btn = ATMButton(num)
                btn.setMinimumWidth(80)
                if num == 'Clear':
                    btn.clicked.connect(self.pin_input.clear)
                else:
                    btn.clicked.connect(lambda _, n=num: self.pin_input.setText(self.pin_input.text() + n))
                keypad_layout.addWidget(btn, i // 3, i % 3)
        card_layout.addLayout(keypad_layout)

        button_layout = QVBoxLayout()
        button_layout.setSpacing(10)
        next_button = ATMButton("Continue")
        next_button.clicked.connect(self.on_next)
        button_layout.addWidget(next_button)

        cancel_button = ATMButton("Cancel")
        cancel_button.clicked.connect(self.on_cancel)
        button_layout.addWidget(cancel_button)

        card_layout.addLayout(button_layout)
        card.setLayout(card_layout)
        layout.addWidget(card)
        layout.addStretch()
        self.setLayout(layout)

    def set_card_number(self, card_number):
        self.card_number = card_number

    def on_cancel(self):
        self.pin_input.clear()
        self.parent.switch_screen(self.parent.card_input_screen)

    def on_next(self):
        pin = self.pin_input.text()
        if len(pin) == 4 and pin.isdigit():
            self.parent.amount_input_screen.set_data(self.card_number, pin)
            self.parent.switch_screen(self.parent.amount_input_screen)
        else:
            dialog = ErrorDialog("Please enter a valid 4-digit PIN")
            dialog.exec()

    def showEvent(self, event):
        super().showEvent(event)
        self.pin_input.setFocus()
        print("PinInputScreen shown, focus set to pin_input")
        fade_in(self)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        print("PinInputScreen gained focus, setting focus to pin_input")
        self.pin_input.setFocus()