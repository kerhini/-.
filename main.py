"""
Главный модуль запуска приложения.
В соответствии с требованиями ТЗ:
- Вся функциональность реализована через методы класса (@staticmethod).
- При закрытии приложения сохраняется отчет о сессии в файл session_report.txt.
"""

import sys
from PyQt6.QtWidgets import QApplication

from login_dialog import LoginDialog
from main_window import InventoryAppWindow


class AppLauncher:
    """Класс запуска и управления жизненным циклом приложения."""

    @staticmethod
    def run():
        """Статический метод запуска приложения (@staticmethod)."""
        app = QApplication(sys.argv)
        app.setStyle("Fusion")

        # 1. Показываем диалог авторизации для фиксации имени пользователя
        login_dialog = LoginDialog("Student_MTI")
        if login_dialog.exec():
            username = login_dialog.login_value
            # 2. Инициализируем и отображаем главное окно приложения
            window = InventoryAppWindow(username)
            window.show()
            sys.exit(app.exec())
        else:
            # Пользователь нажал отмену при входе
            sys.exit(0)


if __name__ == "__main__":
    AppLauncher.run()
