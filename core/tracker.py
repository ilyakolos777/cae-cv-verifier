import cv2
import numpy as np
from typing import Dict, Tuple, Optional


class DeformationTracker:
    def __init__(self, ref_marker_id: int = 0, marker_size_mm: float = 10.0):
        self.ref_marker_id = ref_marker_id
        self.marker_size_mm = marker_size_mm

        # Настройка словаря и детектора ArUco (совместимо с OpenCV 4.7+)
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        self.aruco_params = cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(self.aruco_dict, self.aruco_params)

        self.pixels_per_mm: Optional[float] = None
        self.initial_positions: Dict[int, np.ndarray] = {}

    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, Dict[int, Tuple[float, float]]]:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejected = self.detector.detectMarkers(gray)

        displacements_mm = {}

        if ids is not None:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)

            # Калибровка масштаба по референсному маркеру
            if self.pixels_per_mm is None and self.ref_marker_id in ids:
                idx = np.where(ids == self.ref_marker_id)[0][0]
                ref_corners = corners[idx][0]
                # Вычисление длины стороны маркера в пикселях
                side_len_px = np.linalg.norm(ref_corners[0] - ref_corners[1])
                self.pixels_per_mm = side_len_px / self.marker_size_mm

            # Вычисление центров маркеров и их смещений
            for i, marker_id in enumerate(ids.flatten()):
                center = np.mean(corners[i][0], axis=0)

                if marker_id not in self.initial_positions:
                    self.initial_positions[marker_id] = center

                if self.pixels_per_mm:
                    # Расчет вектора перемещения в пикселях
                    delta_px = center - self.initial_positions[marker_id]
                    # Перевод в миллиметры с учетом оси Y (в OpenCV Y направлена вниз)
                    delta_mm = (delta_px[0] / self.pixels_per_mm, -delta_px[1] / self.pixels_per_mm)
                    displacements_mm[marker_id] = delta_mm

                    # Визуализация вектора перемещения
                    start_pt = tuple(self.initial_positions[marker_id].astype(int))
                    end_pt = tuple(center.astype(int))
                    cv2.arrowedLine(frame, start_pt, end_pt, (0, 0, 255), 2, tipLength=0.3)

        return frame, displacements_mm

    def reset_baseline(self):
        self.initial_positions.clear()
        self.pixels_per_mm = None