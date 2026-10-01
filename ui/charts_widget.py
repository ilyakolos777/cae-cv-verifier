import pyqtgraph as pg
from PyQt6.QtWidgets import QVBoxLayout, QLabel
from PyQt6.QtCore import pyqtSlot
from .custom_controls import CardWidget


class ChartsWidget(CardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.title = QLabel("Аналитика: Реальные перемещения vs МКЭ")
        self.title.setObjectName("H2")
        self.layout.addWidget(self.title)

        # Настройка pyqtgraph для темной темы
        pg.setConfigOption('background', '#181825')
        pg.setConfigOption('foreground', '#cdd6f4')
        pg.setConfigOptions(antialias=True)

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setLabel('left', 'Смещение', units='мм')
        self.plot_widget.setLabel('bottom', 'Кадр')
        self.plot_widget.showGrid(x=True, y=True, alpha=0.2)
        self.layout.addWidget(self.plot_widget, stretch=1)

        # Кривые для графика (красная - CV, синяя - CAE)
        self.pen_cv = pg.mkPen(color='#f38ba8', width=2)
        self.pen_cae = pg.mkPen(color='#89b4fa', width=2, style=pg.QtCore.Qt.PenStyle.DashLine)

        self.curve_cv = self.plot_widget.plot(name="CV (Оптика)", pen=self.pen_cv)
        self.curve_cae = self.plot_widget.plot(name="CAE (МКЭ)", pen=self.pen_cae)

        self.data_x = []
        self.data_cv_y = []
        self.data_cae_y = []

    @pyqtSlot(int, float, float)
    def update_chart(self, frame_idx: int, disp_cv: float, disp_cae: float):
        self.data_x.append(frame_idx)
        self.data_cv_y.append(disp_cv)
        self.data_cae_y.append(disp_cae)

        # Ограничение буфера графика (последние 100 точек)
        max_points = 100
        if len(self.data_x) > max_points:
            self.data_x.pop(0)
            self.data_cv_y.pop(0)
            self.data_cae_y.pop(0)

        self.curve_cv.setData(self.data_x, self.data_cv_y)
        self.curve_cae.setData(self.data_x, self.data_cae_y)

    def clear(self):
        self.data_x.clear()
        self.data_cv_y.clear()
        self.data_cae_y.clear()
        self.curve_cv.setData([], [])
        self.curve_cae.setData([], [])