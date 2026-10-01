from PyQt6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtProperty, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QColor

# Глобальная таблица стилей (QSS) для всего приложения
MODERN_DARK_THEME = """
QWidget {
    background-color: #1e1e2e;
    color: #cdd6f4;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

/* Боковая панель */
#Sidebar {
    background-color: #181825;
    border-right: 1px solid #313244;
}

/* Панели контента (карточки) */
.CardWidget {
    background-color: #272a3a;
    border-radius: 12px;
    border: 1px solid #313244;
}

/* Заголовки */
QLabel#H1 {
    font-size: 24px;
    font-weight: 600;
    color: #cdd6f4;
}
QLabel#H2 {
    font-size: 16px;
    font-weight: 500;
    color: #a6adc8;
}

/* Стандартные кнопки */
QPushButton {
    background-color: #313244;
    color: #cdd6f4;
    border: none;
    border-radius: 8px;
    padding: 10px 16px;
    font-size: 14px;
    font-weight: 500;
}
QPushButton:hover {
    background-color: #45475a;
}
QPushButton:pressed {
    background-color: #585b70;
}

/* Акцентные кнопки (Primary) */
QPushButton.Primary {
    background-color: #89b4fa;
    color: #11111b;
}
QPushButton.Primary:hover {
    background-color: #b4befe;
}
QPushButton.Primary:pressed {
    background-color: #cdd6f4;
}

/* Кнопки опасности (Danger) */
QPushButton.Danger {
    background-color: #f38ba8;
    color: #11111b;
}
QPushButton.Danger:hover {
    background-color: #f5c2e7;
}
"""

class CardWidget(QWidget):
    """Базовый виджет-карточка с закругленными углами для группировки контента"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setProperty("class", "CardWidget")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(16, 16, 16, 16)
        self.layout.setSpacing(10)