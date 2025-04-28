import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QHBoxLayout
from screens.card_input import CardInputScreen
from screens.confirmation import ConfirmationScreen
from screens.amount_input import AmountInputScreen
from screens.pin_input import PinInputScreen
from styles.theme_manager import ThemeManager, ThemeSwitcher

class ATMApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AUT Bank ATM")
        self.setFixedSize(800, 600)

        # Initialize Theme Manager
        self.theme_manager = ThemeManager()
        self.theme_manager.apply_theme(self, "dark")

        # Central widget with stacked screens
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Initialize QStackedWidget
        self.screens = QStackedWidget()
        self.main_layout.addWidget(self.screens)

        # Add screens
        self.card_input_screen = CardInputScreen(self)
        self.pin_input_screen = PinInputScreen(self)
        self.amount_input_screen = AmountInputScreen(self)
        self.confirmation_screen = ConfirmationScreen(self)
        self.screens.addWidget(self.card_input_screen)
        self.screens.addWidget(self.pin_input_screen)
        self.screens.addWidget(self.amount_input_screen)
        self.screens.addWidget(self.confirmation_screen)

        # Add Theme Switcher as a top-level widget
        self.theme_switcher = ThemeSwitcher(self.theme_manager)
        self.theme_switcher.theme_changed.connect(lambda theme_id: self.theme_manager.apply_theme(self, theme_id))
        self.theme_container = QWidget(self)
        self.theme_container.setFixedSize(160, 40)
        self.theme_container.move(630, 10)
        container_layout = QHBoxLayout(self.theme_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(self.theme_switcher)
        self.theme_container.raise_()
        self.theme_switcher.setVisible(True)
        print("ThemeSwitcher added as top-level widget in main.py")

        # Show card input screen
        self.screens.setCurrentWidget(self.card_input_screen)
        # Force initial theme refresh
        self.theme_manager.apply_theme(self, "dark")

    def switch_screen(self, screen):
        self.screens.setCurrentWidget(screen)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ATMApp()
    window.show()
    sys.exit(app.exec())