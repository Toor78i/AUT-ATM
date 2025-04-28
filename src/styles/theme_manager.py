import json
from pathlib import Path
from PySide6.QtWidgets import QComboBox, QVBoxLayout, QWidget, QApplication
from PySide6.QtCore import Signal, Qt


class ThemeManager:
    def __init__(self):
        self.themes = []
        self.current_theme = "dark"
        self.load_themes()

    def load_themes(self):
        theme_path = Path(__file__).parent / "theme.json"
        try:
            with open(theme_path, "r") as file:
                data = json.load(file)
                self.themes = data["themes"]
                print("Loaded themes:", [theme["name"] for theme in self.themes])
        except Exception as e:
            print(f"Error loading themes: {e}")

    def get_theme_variables(self, theme_id):
        theme = next((t for t in self.themes if t["id"] == theme_id), None)
        return theme["variables"] if theme else {}

    def apply_theme(self, app, theme_id):
        self.current_theme = theme_id
        variables = self.get_theme_variables(theme_id)
        if variables:
            stylesheet = generate_stylesheet(variables)
            QApplication.style().unpolish(app)
            app.setStyleSheet(stylesheet)
            for widget in app.findChildren(QWidget):
                QApplication.style().unpolish(widget)
                widget.setStyleSheet(stylesheet)
                widget.style().polish(widget)
            QApplication.style().polish(app)
            print(f"Applied theme: {theme_id} with variables: {variables}")
        else:
            print(f"Theme {theme_id} not found")


def generate_stylesheet(variables):
    return f"""
        QWidget {{
            background-color: {variables.get('--background', '#1E1E2F')};
            color: {variables.get('--foreground', '#E0E7FF')};
            font-family: Inter, Arial, sans-serif;
        }}
        QWidget#card {{
            background-color: {variables.get('--card', '#27293A')};
            border-radius: {variables.get('--radius', '12px')};
            border: 1px solid {variables.get('--border', '#4B5563')};
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        QPushButton {{
            background-color: {variables.get('--primary', '#2DD4BF')};
            color: {variables.get('--primary-foreground', '#27293A')};
            border-radius: {variables.get('--radius', '12px')};
            padding: 12px;
            border: none;
            font-size: 16px;
            font-weight: 500;
        }}
        QPushButton:hover {{
            background-color: {variables.get('--accent', '#3B3E5B')};
        }}
        QPushButton:pressed {{
            background-color: {variables.get('--secondary', '#64748B')};
        }}
        QLineEdit {{
            background-color: {variables.get('--input', '#2D2D44')};
            color: {variables.get('--foreground', '#E0E7FF')};
            border: 1px solid {variables.get('--border', '#4B5563')};
            border-radius: {variables.get('--radius', '12px')};
            padding: 10px;
            font-size: 16px;
        }}
        QLineEdit:focus {{
            border-color: {variables.get('--primary', '#2DD4BF')};
        }}
        QLabel {{
            color: {variables.get('--foreground', '#E0E7FF')};
        }}
        QLabel#title {{
            font-size: 32px;
            font-weight: 700;
        }}
        QLabel#subtitle {{
            font-size: 18px;
            opacity: 0.8;
        }}
        QLabel#label {{
            font-size: 14px;
        }}
        QDialog {{
            background-color: {variables.get('--card', '#27293A')};
            border-radius: {variables.get('--radius', '12px')};
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        QComboBox {{
            background-color: {variables.get('--input', '#2D2D44')};
            color: {variables.get('--foreground', '#E0E7FF')};
            border: 1px solid {variables.get('--border', '#4B5563')};
            border-radius: {variables.get('--radius', '12px')};
            padding: 5px;
            font-size: 14px;
            min-width: 150px;
            min-height: 30px;
        }}
        QComboBox::drop-down {{
            border: none;
            width: 20px;
            background-color: {variables.get('--input', '#2D2D44')};
        }}
        QComboBox::down-arrow {{
            width: 10px;
            height: 10px;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid {variables.get('--foreground', '#E0E7FF')};
        }}
        QComboBox QAbstractItemView {{
            background-color: {variables.get('--card', '#27293A')};
            color: {variables.get('--foreground', '#E0E7FF')};
            selection-background-color: {variables.get('--accent', '#3B3E5B')};
            selection-color: {variables.get('--accent-foreground', '#E0E7FF')};
            border: 1px solid {variables.get('--border', '#4B5563')};
        }}
        QPushButton#keypadButton {{
            background-color: {variables.get('--secondary', '#64748B')};
            border-radius: 10px;
            padding: 15px;
            font-size: 18px;
        }}
        QPushButton#keypadButton:hover {{
            background-color: {variables.get('--accent', '#3B3E5B')};
        }}
        QPushButton#amountButton {{
            background-color: {variables.get('--primary', '#2DD4BF')};
            border-radius: 15px;
            padding: 20px;
            font-size: 20px;
        }}
        QPushButton#amountButton:hover {{
            background-color: {variables.get('--accent', '#3B3E5B')};
        }}
        QLabel#amountLabel {{
            font-size: 24px;
            font-weight: bold;
            color: {variables.get('--primary', '#2DD4BF')};
        }}
        QLabel#referenceLabel {{
            font-size: 16px;
            color: {variables.get('--secondary-foreground', '#E0E7FF')};
        }}
        QProgressBar {{
            border: 2px solid {variables.get('--border', '#4B5563')};
            border-radius: 5px;
            text-align: center;
        }}
        QProgressBar::chunk {{
            background-color: {variables.get('--primary', '#2DD4BF')};
        }}
    """


class ThemeSwitcher(QWidget):
    theme_changed = Signal(str)

    def __init__(self, theme_manager):
        super().__init__()
        self.theme_manager = theme_manager
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.combo = QComboBox()
        self.combo.setMinimumSize(150, 30)
        self.combo.setFocusPolicy(Qt.StrongFocus)
        self.combo.setVisible(True)
        for theme in self.theme_manager.themes:
            self.combo.addItem(theme["name"], theme["id"])
        self.combo.currentIndexChanged.connect(self.on_theme_changed)
        layout.addWidget(self.combo)
        self.setLayout(layout)
        self.raise_()
        print(
            f"ThemeSwitcher initialized at position ({self.pos().x()}, {self.pos().y()}) with themes: {[theme['name'] for theme in self.theme_manager.themes]}"
        )
        self.on_theme_changed()  # Trigger initial theme

    def showEvent(self, event):
        super().showEvent(event)
        print(f"ThemeSwitcher shown at position ({self.pos().x()}, {self.pos().y()})")
        self.combo.setFocus()

    def on_theme_changed(self):
        theme_id = self.combo.currentData()
        if theme_id:
            print(f"Theme switched to: {theme_id}")
            self.theme_changed.emit(theme_id)
        else:
            print("No theme selected")
