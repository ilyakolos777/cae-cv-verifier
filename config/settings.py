import os

# --- Сетевые настройки и MQTT ---
CAM_IP = "192.168.0.196"
STREAM_URL = f"http://{CAM_IP}/mjpeg/1"

MQTT_BROKER = "192.168.0.185"
MQTT_PORT = 1883
TOPIC_COMMAND = "esp32/cam1/command"
TOPIC_STATUS = "esp32/cam1/status"

# --- Настройки компьютерного зрения (OpenCV) ---
CV_SETTINGS = {
    # ArUco маркеры отлично подходят для субпиксельной точности
    "aruco_dict": "DICT_4X4_50",
    "marker_size_mm": 10.0,       # Физический размер распечатанного маркера
    "calibration_file": "data/camera_matrix.npz", # Файл с параметрами дисторсии объектива
    "min_marker_distance": 5.0    # Минимальное расстояние между узлами (защита от шума)
}

# --- Настройки МКЭ (CAE) ---
# Физико-механические характеристики материала (пример: Сталь)
FEM_SETTINGS = {
    "young_modulus": 2e11,        # Модуль Юнга (Па)
    "poisson_ratio": 0.3,         # Коэффициент Пуассона
    "thickness": 0.005,           # Толщина пластины (м)
}

# --- Дизайн интерфейса (PyQt6 Темная тема) ---
UI_COLORS = {
    "bg_main": "#1c1c1e",         # Глубокий темный фон
    "bg_panel": "#2c2c2e",        # Фон панелей и виджетов (stacked)
    "accent": "#0a84ff",          # Акцентный синий
    "success": "#32d74b",         # Зеленый для статусов
    "danger": "#ff453a",          # Красный для ошибок/остановки
    "text_primary": "#ffffff",
    "text_secondary": "#8e8e93",
    "border_radius": 12           # Скругление углов для кастомных кнопок
}

# --- Пути файловой системы ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATHS = {
    "logs": os.path.join(BASE_DIR, "data", "logs"),
    "reports": os.path.join(BASE_DIR, "data", "reports"),
    "snapshots": os.path.join(BASE_DIR, "data", "snapshots"),
    "models": os.path.join(BASE_DIR, "data", "models")
}

# Автоматическое создание структуры папок при старте
for path in PATHS.values():
    os.makedirs(path, exist_ok=True)