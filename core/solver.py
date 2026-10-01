import numpy as np


class PlaneStressSolver:
    def __init__(self, elastic_modulus: float, poisson_ratio: float, thickness: float):
        self.E = elastic_modulus
        self.nu = poisson_ratio
        self.t = thickness
        # Матрица упругости для плоского напряженного состояния
        coef = self.E / (1 - self.nu ** 2)
        self.D = coef * np.array([
            [1, self.nu, 0],
            [self.nu, 1, 0],
            [0, 0, (1 - self.nu) / 2]
        ])

    def calculate_element_stiffness(self, coords: np.ndarray) -> np.ndarray:
        """Расчет локальной матрицы жесткости для трехузлового треугольного элемента (CST)"""
        x1, y1 = coords[0]
        x2, y2 = coords[1]
        x3, y3 = coords[2]

        # Площадь элемента
        area = 0.5 * abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))

        # Матрица градиентов (Strain-Displacement Matrix)
        B = (1 / (2 * area)) * np.array([
            [y2 - y3, 0, y3 - y1, 0, y1 - y2, 0],
            [0, x3 - x2, 0, x1 - x3, 0, x2 - x1],
            [x3 - x2, y2 - y3, x1 - x3, y3 - y1, x2 - x1, y1 - y2]
        ])

        # K_e = t * A * B^T * D * B
        Ke = self.t * area * (B.T @ self.D @ B)
        return Ke

    def assemble_global_matrix(self, num_nodes: int, elements: list, nodes: np.ndarray) -> np.ndarray:
        """Сборка глобальной матрицы жесткости"""
        dof = 2 * num_nodes
        K_global = np.zeros((dof, dof))

        for elem in elements:
            elem_nodes = nodes[elem]
            Ke = self.calculate_element_stiffness(elem_nodes)

            for i in range(3):
                for j in range(3):
                    # Сопоставление локальных и глобальных степеней свободы
                    global_i = [2 * elem[i], 2 * elem[i] + 1]
                    global_j = [2 * elem[j], 2 * elem[j] + 1]

                    K_global[np.ix_(global_i, global_j)] += Ke[2 * i:2 * i + 2, 2 * j:2 * j + 2]

        return K_global

    def solve(self, K_global: np.ndarray, forces: np.ndarray, constrained_dofs: list) -> np.ndarray:
        """Решение системы K*U = F с учетом граничных условий"""
        dof = K_global.shape[0]
        free_dofs = np.setdiff1d(np.arange(dof), constrained_dofs)

        # Редукция матриц по свободным степеням свободы
        K_reduced = K_global[np.ix_(free_dofs, free_dofs)]
        F_reduced = forces[free_dofs]

        # Вычисление перемещений
        U_reduced = np.linalg.solve(K_reduced, F_reduced)

        # Восстановление полного вектора перемещений
        U_full = np.zeros(dof)
        U_full[free_dofs] = U_reduced
        return U_full