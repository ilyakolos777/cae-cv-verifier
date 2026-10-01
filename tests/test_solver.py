import pytest
import numpy as np
from core.solver import PlaneStressSolver

# 64 теста: проверка свойств матрицы упругости для разных материалов
@pytest.mark.parametrize("E", [2e5, 7e4, 1e5, 6.9e4])
@pytest.mark.parametrize("nu", [0.25, 0.3, 0.33, 0.35])
@pytest.mark.parametrize("t", [1.0, 2.5, 5.0, 10.0])
def test_elastic_matrix_properties(E, nu, t):
    solver = PlaneStressSolver(E, nu, t)
    assert solver.D.shape == (3, 3)
    # Матрица должна быть положительно определенной и симметричной
    assert np.all(np.linalg.eigvals(solver.D) > 0)
    assert np.allclose(solver.D, solver.D.T)

# 9 тестов: проверка размерности глобальной матрицы жесткости
@pytest.mark.parametrize("node_count", [3, 10, 25, 50, 100, 250, 500, 1000, 5000])
def test_global_matrix_dimensions(node_count):
    solver = PlaneStressSolver(2e5, 0.3, 5.0)
    expected_dof = node_count * 2
    K = solver.assemble_global_matrix(node_count, [], np.zeros((node_count, 2)))
    assert K.shape == (expected_dof, expected_dof)