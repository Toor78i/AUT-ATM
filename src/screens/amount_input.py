from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QLineEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QDoubleValidator
from components.button import ATMButton
from components.error_dialog import ErrorDialog
from utils.animations import fade_in


class AmountInputScreen(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.card_number = ""
        self.pin = ""
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

        title = QLabel("Select or Enter Amount")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)

        amounts = [20, 50, 100, 200]
        grid = QGridLayout()
        grid.setSpacing(20)  # Increased spacing
        for i, amount in enumerate(amounts):
            btn = ATMButton(f"${amount}")
            btn.setObjectName("amountButton")  # Set object name for styling
            btn.setMinimumWidth(120)  # Increased size
            btn.clicked.connect(lambda _, a=amount: self.amount_input.setText(str(a)))
            grid.addWidget(btn, i // 2, i % 2)
        card_layout.addLayout(grid)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Enter amount")
        self.amount_input.setAlignment(Qt.AlignCenter)
        self.amount_input.setMinimumWidth(350)  # Increased width
        validator = QDoubleValidator(0.0, 10000.0, 2)
        validator.setNotation(QDoubleValidator.StandardNotation)
        self.amount_input.setValidator(validator)
        card_layout.addWidget(self.amount_input)

        button_layout = QVBoxLayout()
        button_layout.setSpacing(10)
        withdraw_button = ATMButton("Withdraw")
        withdraw_button.clicked.connect(self.on_withdraw)
        button_layout.addWidget(withdraw_button)

        cancel_button = ATMButton("Cancel")
        cancel_button.clicked.connect(self.on_cancel)
        button_layout.addWidget(cancel_button)

        card_layout.addLayout(button_layout)
        card.setLayout(card_layout)
        card.setMinimumWidth(500)  # Set minimum width for card
        layout.addWidget(card)
        layout.addStretch()
        self.setLayout(layout)

    def set_data(self, card_number, pin):
        self.card_number = card_number
        self.pin = pin

    def on_cancel(self):
        self.amount_input.clear()
        self.parent.switch_screen(self.parent.card_input_screen)

    def on_withdraw(self):
        amount = self.amount_input.text()
        try:
            amount_float = float(amount)
            if amount_float > 0:
                self.parent.confirmation_screen.set_data(
                    self.card_number, self.pin, amount_float
                )
                self.parent.switch_screen(self.parent.confirmation_screen)
            else:
                dialog = ErrorDialog("Please enter a positive amount")
                dialog.exec()
        except ValueError:
            dialog = ErrorDialog("Please enter a valid number")
            dialog.exec()

    def showEvent(self, event):
        super().showEvent(event)
        fade_in(self)
