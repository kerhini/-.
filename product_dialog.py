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


# Диалоговое окно для создания и изменения товара
class ProductEditDialog(CustomDialog):

    def __init__(self, product: Product = None, parent=None):
        title = "Редактирование товара" if product else "Новый товар"
        super().__init__(title, parent)
        self.setMinimumWidth(440)
        self._target_product = product

        self._init_ui()
        if product:
            self._fill_data(product)

    def _init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(10)

        # Выравнивание полей формы
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        form_layout.setSpacing(8)

        # Поля ввода
        self.input_id = CustomSpinBox(1, 999999, 1)
        self.input_id.setDecimals(0)
        if self._target_product:
            # При редактировании ID менять нельзя
            self.input_id.setEnabled(False)

        self.input_name = CustomLineEdit("Введите наименование...")

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

        self.input_description = CustomTextEdit("Описание товара...")
        self.input_description.setMaximumHeight(80)

        # Добавляем поля в форму
        form_layout.addRow(CustomLabel("ID:"), self.input_id)
        form_layout.addRow(CustomLabel("Название:"), self.input_name)
        form_layout.addRow(CustomLabel("Категория:"), self.combo_category)
        form_layout.addRow(CustomLabel("Цена:"), self.input_price)
        form_layout.addRow(CustomLabel("Количество:"), self.input_quantity)
        form_layout.addRow(CustomLabel("Штрихкод:"), self.input_barcode)
        form_layout.addRow(CustomLabel("Рейтинг:"), self.input_rating)
        form_layout.addRow(CustomLabel("Описание:"), self.input_description)

        main_layout.addLayout(form_layout)

        # Нижние кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(8)
        buttons_layout.addStretch()

        self.btn_cancel = CustomButton("Отмена")
        self.btn_cancel.clicked.connect(self.reject)
        buttons_layout.addWidget(self.btn_cancel)

        self.btn_save = CustomButton("Сохранить", primary=True)
        self.btn_save.clicked.connect(self._on_save)
        buttons_layout.addWidget(self.btn_save)

        main_layout.addLayout(buttons_layout)
        self.setLayout(main_layout)

    def _fill_data(self, product: Product):
        # Заполняем форму значениями существующего товара
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

    def _on_save(self):
        # Простая валидация перед сохранением
        name = self.input_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Предупреждение", "Заполните название товара!")
            return

        barcode = self.input_barcode.text().strip()
        if not barcode:
            QMessageBox.warning(self, "Предупреждение", "Заполните штрихкод товара!")
            return

        self.accept()

    def get_product(self) -> Product:
        # Собираем введенные данные в объект Product
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
