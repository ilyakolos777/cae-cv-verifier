import os
from datetime import datetime
import pandas as pd
from config.settings import PATHS


class VerificationExporter:
    def __init__(self):
        self.reports_dir = PATHS["reports"]

    def export_to_excel(self, real_coords: dict, fem_coords: dict, nodes_info: dict) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.reports_dir, f"CAE_Verification_{timestamp}.xlsx")

        data = []
        for node_id in real_coords.keys():
            x0, y0 = nodes_info.get(node_id, (0, 0))
            dx_r, dy_r = real_coords[node_id]
            dx_f, dy_f = fem_coords.get(node_id, (0.0, 0.0))

            # Вычисление абсолютной невязки
            err_x = abs(dx_r - dx_f)
            err_y = abs(dy_r - dy_f)

            data.append({
                "ID Маркера (Узел)": node_id,
                "Нач. коорд. X (мм)": round(x0, 2),
                "Нач. коорд. Y (мм)": round(y0, 2),
                "Смещение CV dX (мм)": round(dx_r, 4),
                "Смещение CV dY (мм)": round(dy_r, 4),
                "Смещение МКЭ dX (мм)": round(dx_f, 4),
                "Смещение МКЭ dY (мм)": round(dy_f, 4),
                "Абс. погрешность dX": round(err_x, 4),
                "Абс. погрешность dY": round(err_y, 4)
            })

        df = pd.DataFrame(data)

        # Вычисление сводной статистики для второго листа
        summary_data = {
            "Метрика": ["Средняя погрешность X", "Средняя погрешность Y", "Макс. погрешность X", "Макс. погрешность Y"],
            "Значение (мм)": [
                round(df["Абс. погрешность dX"].mean(), 4),
                round(df["Абс. погрешность dY"].mean(), 4),
                round(df["Абс. погрешность dX"].max(), 4),
                round(df["Абс. погрешность dY"].max(), 4)
            ]
        }
        df_summary = pd.DataFrame(summary_data)

        # Экспорт с использованием openpyxl для стилизации
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name="Узловые перемещения", index=False)
            df_summary.to_excel(writer, sheet_name="Сводная статистика", index=False)

            # Автоматическая настройка ширины колонок для всех листов
            for sheet_name in writer.sheets:
                worksheet = writer.sheets[sheet_name]
                for col in worksheet.columns:
                    max_length = 0
                    column_letter = col[0].column_letter
                    for cell in col:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    # Устанавливаем ширину с небольшим запасом
                    worksheet.column_dimensions[column_letter].width = max_length + 2

        return filename