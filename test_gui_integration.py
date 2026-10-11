"""
Интеграционный тест графического интерфейса пользователя (PyQt6).
Запускается в режиме offscreen для проверки реальной отрисовки,
фильтрации, сортировки и сохранения отчета при закрытии.
"""

import os
import sys
from datetime import datetime
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from main_window import InventoryAppWindow
from report_generator import SessionReportGenerator


class GuiIntegrationTester:
    """Класс для проверки работы GUI-компонентов (@staticmethod)."""

    @staticmethod
    def run_test():
        os.environ["QT_QPA_PLATFORM"] = "offscreen"
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)

        window = InventoryAppWindow(username="TestStudent")
        window.show()

        # 1. Проверка начального состояния таблицы
        initial_row_count = window.table.rowCount()
        assert initial_row_count == 12, f"Ожидалось 12 строк, получено {initial_row_count}"

        # 2. Проверка работы поиска
        window.search_input.setText("ThinkPad")
        assert window.table.rowCount() == 1, f"Ожидалась 1 строка после поиска, получено {window.table.rowCount()}"

        # 3. Сброс фильтра
        window._reset_filters()
        assert window.table.rowCount() == 12

        # 4. Проверка фильтрации по категории
        window.combo_category.setCurrentText("Периферия")
        assert window.table.rowCount() == 3, f"Ожидалось 3 товара периферии, получено {window.table.rowCount()}"

        # 5. Проверка сортировки по цене
        window._reset_filters()
        window._sort_by_price()
        # Проверяем, что первая строка содержит товар с наименьшей ценой (USB-C кабель, 2490 руб.)
        first_item_name = window.table.item(0, 1).text()
        assert "USB-C" in first_item_name, f"Первым должен быть самый дешевый товар, но получен {first_item_name}"

        # 6. Проверка закрытия и сохранения отчета сессии
        report_file = "session_report.txt"
        if os.path.exists(report_file):
            os.remove(report_file)

        window.close()

        assert os.path.exists(report_file), "Файл session_report.txt не был создан при закрытии окна!"
        with open(report_file, "r", encoding="utf-8") as f:
            content = f.read()

        assert "+-" in content
        assert "login" in content
        assert "time_in" in content
        assert "time_out" in content
        assert "TestStudent" in content
        print("\nСодержимое сохраненного отчета при выходе:")
        print(content)

        print("[OK] Интеграционный тест GUI успешно завершен!")


if __name__ == "__main__":
    GuiIntegrationTester.run_test()
