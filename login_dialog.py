"""Диалоговое окно входа пользователя."""

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


class LoginDialog(CustomDialog):
    """Окно авторизации пользователя."""

    def __init__(self, default_login: str = "admin", parent=None):
        super().__init__("Авторизация", parent)
        self.setFixedSize(360, 180)
        self._login_value = default_login
        self._init_ui(default_login)

    @property
    def login_value(self) -> str:
        return self._login_value

    def _init_ui(self, default_login: str):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        title_label = CustomLabel("Вход в систему складского учёта", is_title=True)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.login_input = CustomLineEdit("Введите ваш логин")
        self.login_input.setText(default_login)
        form_layout.addRow(CustomLabel("Логин:"), self.login_input)
        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.btn_exit = CustomButton("Выход", primary=False)
        self.btn_exit.clicked.connect(self.reject)
        button_layout.addWidget(self.btn_exit)

        self.btn_submit = CustomButton("Войти", primary=True)
        self.btn_submit.clicked.connect(self._on_submit)
        button_layout.addWidget(self.btn_submit)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.login_input.enter_pressed_signal.connect(self._on_submit)

    def _on_submit(self):
        entered = self.login_input.text().strip()
        if not entered:
            QMessageBox.warning(self, "Ошибка", "Логин не может быть пустым!")
            return
        self._login_value = entered
        self.accept()
