import sys
from PyQt6.QtWidgets import QApplication

from login_dialog import LoginDialog
from main_window import InventoryAppWindow


# Класс для запуска приложения
class AppLauncher:

    @staticmethod
    def run():
        app = QApplication(sys.argv)
        app.setStyle("Fusion")

        # Открываем окно входа для получения логина пользователя
        login_dialog = LoginDialog("admin")
        if login_dialog.exec():
            username = login_dialog.login_value
            # Создаем и показываем главное окно
            window = InventoryAppWindow(username)
            window.show()
            sys.exit(app.exec())
        else:
            # Если пользователь отменил вход, просто закрываем
            sys.exit(0)


if __name__ == "__main__":
    AppLauncher.run()
