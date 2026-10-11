"""Модуль запуска приложения."""

import sys
from PyQt6.QtWidgets import QApplication

from login_dialog import LoginDialog
from main_window import InventoryAppWindow


class AppLauncher:
    """Запуск и управление жизненным циклом приложения."""

    @staticmethod
    def run():
        app = QApplication(sys.argv)
        app.setStyle("Fusion")

        login_dialog = LoginDialog("admin")
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
