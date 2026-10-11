"""Диалоговое окно добавления и редактирования товара."""

from PyQt6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QVBoxLayout,
    QMessageBox,
)
from PyQt6.QtCore import Qt

from custom_widgets import (
    CustomDialog,
    CustomButton,
    CustomLineEdit,
    CustomComboBox,
    CustomSpinBox,
    CustomTextEdit,
    CustomLabel,
)
from entities import Product


class ProductEditDialog(CustomDialog):
    """Диалоговое окно создания/редактирования сущности Product."""

    def __init__(self, product: Product = None, parent=None):
        title = "Редактирование товара" if product else "Новый товар"
        super().__init__(title, parent)
        self.setMinimumWidth(450)
        self._target_product = product

        self._init_ui()
        if product:
            self._fill_data(product)

    def _init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(18, 18, 18, 18)
        main_layout.setSpacing(12)

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        form_layout.setSpacing(10)

        # Поля ввода на базе переопределенных компонентов
        self.input_id = CustomSpinBox(1, 999999, 1)
        self.input_id.setDecimals(0)
        if self._target_product:
            self.input_id.setEnabled(False)

        self.input_name = CustomLineEdit("Введите наименование товара")
        
        self.combo_category = CustomComboBox()
        categories = list()
        categories.append("Электроника")
        categories.append("Периферия")
        categories.append("Аудио")
        categories.append("Хранение данных")
        categories.append("Сетевое оборудование")
        categories.append("Аксессуары")
        categories.append("Питание")
        for cat in categories:
            self.combo_category.addItem(cat)

        self.input_price = CustomSpinBox(0.0, 1000000.0, 10.0)
        self.input_price.setDecimals(2)
        self.input_price.setSuffix(" руб.")

        self.input_quantity = CustomSpinBox(0, 100000, 1)
        self.input_quantity.setDecimals(0)
        self.input_quantity.setSuffix(" шт.")

        self.input_barcode = CustomLineEdit("4600000000000")

        self.input_rating = CustomSpinBox(0.0, 5.0, 0.1)
        self.input_rating.setDecimals(1)
        self.input_rating.setValue(5.0)

        self.input_description = CustomTextEdit("Подробное описание товара...")
        self.input_description.setMaximumHeight(80)

        # Добавление строк формы с выравниванием
        form_layout.addRow(CustomLabel("ID товара:"), self.input_id)
        form_layout.addRow(CustomLabel("Наименование:"), self.input_name)
        form_layout.addRow(CustomLabel("Категория:"), self.combo_category)
        form_layout.addRow(CustomLabel("Цена:"), self.input_price)
        form_layout.addRow(CustomLabel("Количество:"), self.input_quantity)
        form_layout.addRow(CustomLabel("Штрихкод:"), self.input_barcode)
        form_layout.addRow(CustomLabel("Рейтинг:"), self.input_rating)
        form_layout.addRow(CustomLabel("Описание:"), self.input_description)

        main_layout.addLayout(form_layout)

        # Панель кнопок сохранения/отмены
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        button_layout.addStretch()

        self.btn_cancel = CustomButton("Отмена", primary=False)
        self.btn_cancel.clicked.connect(self.reject)
        button_layout.addWidget(self.btn_cancel)

        self.btn_save = CustomButton("Сохранить", primary=True)
        self.btn_save.clicked.connect(self._on_save_clicked)
        button_layout.addWidget(self.btn_save)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def _fill_data(self, product: Product):
        self.input_id.setValue(product.id)
        self.input_name.setText(product.name)
        idx = self.combo_category.findText(product.category)
        if idx >= 0:
            self.combo_category.setCurrentIndex(idx)
        self.input_price.setValue(product.price)
        self.input_quantity.setValue(product.quantity)
        self.input_barcode.setText(product.barcode)
        self.input_rating.setValue(product.rating)
        self.input_description.setPlainText(product.description)

    def _on_save_clicked(self):
        name = self.input_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка ввода", "Наименование товара не может быть пустым!")
            return

        barcode = self.input_barcode.text().strip()
        if not barcode:
            QMessageBox.warning(self, "Ошибка ввода", "Штрихкод не может быть пустым!")
            return

        self.accept()

    def get_product(self) -> Product:
        """Сформировать и вернуть объект Product."""
        return Product(
            product_id=int(self.input_id.value()),
            name=self.input_name.text().strip(),
            category=self.combo_category.currentText(),
            price=float(self.input_price.value()),
            quantity=int(self.input_quantity.value()),
            barcode=self.input_barcode.text().strip(),
            rating=float(self.input_rating.value()),
            description=self.input_description.toPlainText().strip(),
        )
