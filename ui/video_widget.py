import cv2
import numpy as np
from PyQt6.QtWidgets import QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QImage, QPixmap
from .custom_controls import CardWidget


class VideoWidget(CardWidget):
    # Сигнал для потокобезопасного обновления UI из вычислительного ядра
    frame_received = pyqtSignal(np.ndarray)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.title = QLabel("Live: Деформация образца")
        self.title.setObjectName("H2")
        self.layout.addWidget(self.title)

        self.video_label = QLabel("Ожидание потока...")
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setStyleSheet("background-color: #11111b; border-radius: 8px;")
        self.video_label.setMinimumSize(640, 480)
        self.layout.addWidget(self.video_label, stretch=1)

        self.frame_received.connect(self.update_frame)

    @pyqtSlot(np.ndarray)
    def update_frame(self, frame: np.ndarray):
        if frame is None:
            return

        # Конвертация BGR (OpenCV) в RGB (PyQt)
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w

        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)

        # Масштабирование под размер окна с сохранением пропорций
        scaled_pixmap = pixmap.scaled(
            self.video_label.width(),
            self.video_label.height(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.video_label.setPixmap(scaled_pixmap)

    def clear(self):
        self.video_label.clear()
        self.video_label.setText("Поток остановлен")