from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt
from components.button import ATMButton
from components.error_dialog import ErrorDialog
from api.client import APIClient
from utils.animations import fade_in


class ConfirmationScreen(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.api_client = APIClient()
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(40, 40, 40, 40)
        self.setLayout(self.layout)

    def set_data(self, card_number, pin, amount):
        self.clear()
        self.show_loading()
        result = self.api_client.withdraw(card_number, pin, float(amount))
        if "error" in result:
            self.show_error(result["error"])
        else:
            self.show_success(result)

    def show_loading(self):
        self.clear()
        card = QWidget()
        card.setObjectName("card")
        card_layout = QVBoxLayout()
        card_layout.setAlignment(Qt.AlignCenter)
        card_layout.setContentsMargins(30, 30, 30, 30)

        progress = QProgressBar()
        progress.setRange(0, 0)  # Indeterminate mode
        progress.setTextVisible(False)
        card_layout.addWidget(progress)

        card.setLayout(card_layout)
        card.setMinimumWidth(500)  # Set minimum width for card
        self.layout.addWidget(card)
        self.layout.addStretch()

    def show_success(self, data):
        self.clear()
        card = QWidget()
        card.setObjectName("card")
        card_layout = QVBoxLayout()
        card_layout.setAlignment(Qt.AlignCenter)
        card_layout.setSpacing(15)
        card_layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel("Withdrawal Successful")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)

        amount_label = QLabel(f"Amount: ${data['Amount']:.2f}")
        amount_label.setObjectName("amountLabel")
        amount_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(amount_label)

        reference_label = QLabel(f"Reference: {data['ReferenceNumber']}")
        reference_label.setObjectName("referenceLabel")
        reference_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(reference_label)

        done_button = ATMButton("Done")
        done_button.setMinimumWidth(200)
        done_button.clicked.connect(self.on_done)
        card_layout.addWidget(done_button)

        card.setLayout(card_layout)
        card.setMinimumWidth(500)  # Set minimum width for card
        self.layout.addWidget(card)
        self.layout.addStretch()

    def show_error(self, message):
        dialog = ErrorDialog(message)
        dialog.finished.connect(self.on_done)
        dialog.exec()

    def clear(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def on_done(self):
        self.parent.switch_screen(self.parent.card_input_screen)

    def showEvent(self, event):
        super().showEvent(event)
        fade_in(self)
