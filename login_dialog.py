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


# Окно авторизации перед запуском программы
class LoginDialog(CustomDialog):

    def __init__(self, default_login="admin", parent=None):
        super().__init__("Вход в систему", parent)
        self.setFixedSize(340, 160)
        self._login_value = default_login
        self._init_ui(default_login)

    @property
    def login_value(self):
        return self._login_value

    def _init_ui(self, default_login):
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Заголовок окна
        title_label = CustomLabel("Авторизация", is_title=True)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Поле для ввода логина
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.login_input = CustomLineEdit("Введите ваш логин...")
        self.login_input.setText(default_login)
        form_layout.addRow(CustomLabel("Логин:"), self.login_input)
        layout.addLayout(form_layout)

        # Кнопки входа и отмены
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

        # По нажатию Enter тоже логинимся
        self.login_input.enter_pressed_signal.connect(self._on_login)

    def _on_login(self):
        login = self.login_input.text().strip()
        if not login:
            QMessageBox.warning(self, "Ошибка", "Логин не может быть пустым!")
            return
        self._login_value = login
        self.accept()
