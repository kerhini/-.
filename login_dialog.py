from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QMessageBox,
)
from PyQt6.QtCore import Qt
from custom_widgets import (
    CustomDialog,
    CustomButton,
    CustomLineEdit,
    CustomLabel,
)


# Окно авторизации пользователя перед началом работы
class LoginDialog(CustomDialog):

    def __init__(self, default_login: str = "admin", parent=None):
        super().__init__("Авторизация", parent)
        self.setFixedSize(340, 170)
        self._login_value = default_login
        self._init_ui(default_login)

    @property
    def login_value(self) -> str:
        return self._login_value

    def _init_ui(self, default_login: str):
        layout = QVBoxLayout()
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        # Заголовок
        title_label = CustomLabel("Вход в систему", is_title=True)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Форма ввода логина
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.login_input = CustomLineEdit("Введите имя пользователя...")
        self.login_input.setText(default_login)
        form_layout.addRow(CustomLabel("Логин:"), self.login_input)
        layout.addLayout(form_layout)

        # Кнопки
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)

        self.btn_cancel = CustomButton("Отмена")
        self.btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(self.btn_cancel)

        self.btn_login = CustomButton("Войти", primary=True)
        self.btn_login.clicked.connect(self._on_login)
        btn_layout.addWidget(self.btn_login)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

        # Вход по нажатию Enter
        self.login_input.enter_pressed_signal.connect(self._on_login)

    def _on_login(self):
        login = self.login_input.text().strip()
        if not login:
            QMessageBox.warning(self, "Ошибка", "Введите логин!")
            return
        self._login_value = login
        self.accept()
