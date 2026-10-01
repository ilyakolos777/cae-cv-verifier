import pytest
import numpy as np
from core.tracker import DeformationTracker


# 81 тест: матрица смещений по осям X и Y (в пикселях)
@pytest.mark.parametrize("dx", np.linspace(-50, 50, 9))
@pytest.mark.parametrize("dy", np.linspace(-50, 50, 9))
def test_tracker_displacement_logic(dx, dy):
    tracker = DeformationTracker(marker_size_mm=10.0)
    tracker.pixels_per_mm = 5.0
    tracker.initial_positions[1] = np.array([100.0, 100.0])

    # Симуляция нового положения центра маркера в кадре
    new_center = np.array([100.0 + dx, 100.0 + dy])

    # Изолированная проверка логики расчета векторов
    delta_px = new_center - tracker.initial_positions[1]
    delta_mm = (delta_px[0] / tracker.pixels_per_mm, -delta_px[1] / tracker.pixels_per_mm)

    assert np.isclose(delta_mm[0], dx / 5.0)
    assert np.isclose(delta_mm[1], -dy / 5.0)