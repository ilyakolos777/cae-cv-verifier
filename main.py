import sys
import numpy as np
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QColor

# Импорт конфигурации и ядра
from config.settings import STREAM_URL
from core.camera import CameraStream
from core.tracker import DeformationTracker

# Импорт интерфейса
from ui.main_window import MainWindow


class StreamWorker(QThread):
    """
    Рабочий поток для асинхронного захвата видео,
    поиска маркеров и расчета деформаций в фоне.
    """
    frame_ready = pyqtSignal(np.ndarray)
    metrics_ready = pyqtSignal(int, float, float)

    def __init__(self):
        super().__init__()
        self.is_running = True
        self.camera = CameraStream(STREAM_URL)
        self.tracker = DeformationTracker()
        self.frame_idx = 0

    def run(self):
        if not self.camera.connect():
            print("Ошибка: Нет сигнала от ESP-32 CAM")
            return

        for frame, _ in self.camera.get_frames():
            if not self.is_running:
                break

            processed_frame, displacements = self.tracker.process_frame(frame)
            self.frame_ready.emit(processed_frame)

            if displacements and 0 in displacements:
                dx, dy = displacements[0]
                real_disp = (dx ** 2 + dy ** 2) ** 0.5

                # Эмуляция расчетного смещения (до подключения модуля solver)
                cae_disp = real_disp * 0.95

                self.metrics_ready.emit(self.frame_idx, real_disp, cae_disp)

            self.frame_idx += 1

        self.camera.disconnect()

    def stop(self):
        self.is_running = False
        self.wait()


class AppController(MainWindow):
    """
    Контроллер приложения. Связывает кнопки с логикой.
    """

    def __init__(self):
        super().__init__()
        self.worker = None

        # Подключаем нажатие кнопки к методу запуска
        self.btn_stream.clicked.connect(self.toggle_processing)

    def toggle_processing(self):
        self.is_streaming = not self.is_streaming

        if self.is_streaming:
            self.btn_stream.setText("Stop Stream")
            self.btn_stream.base_color = QColor("#FF453A")
            self.btn_stream.hover_color = QColor("#FF6961")
            self.btn_stream.update_stylesheet(self.btn_stream.base_color)
            self.lbl_status.setText("Status: Processing")

            self.worker = StreamWorker()
            self.worker.frame_ready.connect(self.video_widget.update_frame)
            self.worker.metrics_ready.connect(self.charts_widget.update_chart)

            self.worker.start()
        else:
            self.btn_stream.setText("Start Stream")
            self.btn_stream.base_color = QColor("#0A84FF")
            self.btn_stream.hover_color = QColor("#409CFF")
            self.btn_stream.update_stylesheet(self.btn_stream.base_color)
            self.lbl_status.setText("Status: Idle")

            if self.worker is not None:
                self.worker.stop()
                self.worker = None
            self.video_widget.clear()


# Глобальная ссылка, чтобы сборщик мусора не удалил окно (особенность PyQt на macOS)
window = None


def main():
    global window
    app = QApplication(sys.argv)

    # Системный шрифт Apple (SF Pro) подхватится автоматически
    font = app.font()
    font.setPointSize(14)
    app.setFont(font)

    window = AppController()
    window.show()

    sys.exit(app.exec())


# Точка входа в скрипт (без этого программа завершится с кодом 0)
if __name__ == "__main__":
    main()