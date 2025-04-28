from PySide6.QtCore import QPropertyAnimation

def fade_in(widget):
    animation = QPropertyAnimation(widget, b"windowOpacity")
    animation.setDuration(500)
    animation.setStartValue(0)
    animation.setEndValue(1)
    animation.start()