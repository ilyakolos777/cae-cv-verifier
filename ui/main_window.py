from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                             QPushButton, QLabel, QFrame)
from PyQt6.QtCore import Qt, QThread
from .custom_controls import MODERN_DARK_THEME
from .video_widget import VideoWidget
from .charts_widget import ChartsWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CAE Verification Node")
        self.setMinimumSize(1280, 720)
        self.setStyleSheet(MODERN_DARK_THEME)

        # Главный контейнер
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # === Левая панель управления (Sidebar) ===
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(280)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 30, 20, 30)
        sidebar_layout.setSpacing(15)

        title = QLabel("Управление узлом")
        title.setObjectName("H1")
        title.setWordWrap(True)
        sidebar_layout.addWidget(title)

        self.lbl_status = QLabel("Статус: Ожидание")
        self.lbl_status.setStyleSheet("color: #a6adc8;")
        sidebar_layout.addWidget(self.lbl_status)

        sidebar_layout.addSpacing(20)

        self.btn_stream = QPushButton("▶ Запуск потока")
        self.btn_stream.setProperty("class", "Primary")
        self.btn_stream.clicked.connect(self.toggle_stream)
        sidebar_layout.addWidget(self.btn_stream)

        self.btn_calibrate = QPushButton(" Калибровка маркеров")
        sidebar_layout.addWidget(self.btn_calibrate)

        self.btn_mqtt = QPushButton(" Синхронизация MQTT")
        sidebar_layout.addWidget(self.btn_mqtt)

        sidebar_layout.addStretch()

        self.btn_export = QPushButton(" Экспорт отчета (Excel)")
        self.btn_export.setProperty("class", "Primary")
        sidebar_layout.addWidget(self.btn_export)

        main_layout.addWidget(sidebar)

        # === Правая рабочая область (Рабочий стол) ===
        workspace = QWidget()
        workspace_layout = QVBoxLayout(workspace)
        workspace_layout.setContentsMargins(20, 20, 20, 20)
        workspace_layout.setSpacing(20)

        # Виджет видео (верхняя часть)
        self.video_widget = VideoWidget()
        workspace_layout.addWidget(self.video_widget, stretch=3)

        # Виджет графиков (нижняя часть)
        self.charts_widget = ChartsWidget()
        workspace_layout.addWidget(self.charts_widget, stretch=2)

        main_layout.addWidget(workspace)

        # Внутренние флаги состояния
        self.is_streaming = False

    def toggle_stream(self):
        self.is_streaming = not self.is_streaming
        if self.is_streaming:
            self.btn_stream.setText(" Остановка потока")
            self.btn_stream.setProperty("class", "Danger")
            self.lbl_status.setText("Статус: Трансляция активна")
            # TODO: Запуск QThread с core.CameraStream здесь
        else:
            self.btn_stream.setText(" Запуск потока")
            self.btn_stream.setProperty("class", "Primary")
            self.lbl_status.setText("Статус: Ожидание")
            self.video_widget.clear()
            # TODO: Остановка QThread здесь

        # Принудительное обновление стилей кнопки после смены класса
        self.btn_stream.style().unpolish(self.btn_stream)
        self.btn_stream.style().polish(self.btn_stream)