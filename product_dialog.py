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


# Окно добавления или изменения данных о товаре
class ProductEditDialog(CustomDialog):

    def __init__(self, product=None, parent=None):
        if product:
            title = "Редактирование товара"
        else:
            title = "Добавление товара"
        super().__init__(title, parent)
        self.setMinimumWidth(420)
        self._target_product = product

        self._init_ui()
        if product:
            self._fill_data(product)

    def _init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(14, 14, 14, 14)
        main_layout.setSpacing(10)

        # Разметка полей формы
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        form_layout.setSpacing(8)

        # Поля для ввода
        self.input_id = CustomSpinBox(1, 999999, 1)
        self.input_id.setDecimals(0)
        if self._target_product:
            # При редактировании не даем менять ID
            self.input_id.setEnabled(False)

        self.input_name = CustomLineEdit("Наименование товара...")

        self.combo_category = CustomComboBox()
        cats = list()
        cats.append("Электроника")
        cats.append("Периферия")
        cats.append("Аудио")
        cats.append("Хранение данных")
        cats.append("Сетевое оборудование")
        cats.append("Аксессуары")
        cats.append("Питание")
        for c in cats:
            self.combo_category.addItem(c)

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

        # Добавляем все поля в форму
        form_layout.addRow(CustomLabel("ID:"), self.input_id)
        form_layout.addRow(CustomLabel("Название:"), self.input_name)
        form_layout.addRow(CustomLabel("Категория:"), self.combo_category)
        form_layout.addRow(CustomLabel("Цена:"), self.input_price)
        form_layout.addRow(CustomLabel("Количество:"), self.input_quantity)
        form_layout.addRow(CustomLabel("Штрихкод:"), self.input_barcode)
        form_layout.addRow(CustomLabel("Рейтинг:"), self.input_rating)
        form_layout.addRow(CustomLabel("Описание:"), self.input_description)

        main_layout.addLayout(form_layout)

        # Кнопки сохранения и отмены
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        btn_layout.addStretch()

        self.btn_cancel = CustomButton("Отмена")
        self.btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(self.btn_cancel)

        self.btn_save = CustomButton("Сохранить", primary=True)
        self.btn_save.clicked.connect(self._on_save)
        btn_layout.addWidget(self.btn_save)

        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)

    def _fill_data(self, product):
        # Заполняем поля данными выбранного товара
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
        # Проверяем, что заполнено название
        name = self.input_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Внимание", "Введите название товара!")
            return

        barcode = self.input_barcode.text().strip()
        if not barcode:
            QMessageBox.warning(self, "Внимание", "Введите штрихкод товара!")
            return

        self.accept()

    def get_product(self):
        # Возвращаем созданный объект товара
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
