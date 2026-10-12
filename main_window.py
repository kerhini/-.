from datetime import datetime

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QHeaderView,
    QTableWidgetItem,
    QMessageBox,
    QSplitter,
    QLabel,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from custom_map import CustomMap
from entities import Product, ProductRepository
from custom_widgets import (
    CustomMainWindow,
    CustomButton,
    CustomLineEdit,
    CustomLabel,
    CustomTableWidget,
    CustomComboBox,
    CustomCheckBox,
    CustomProgressBar,
    CustomTextEdit,
    CustomGroupBox,
    CustomStatusBar,
)
from product_dialog import ProductEditDialog
from report_generator import SessionRecord, SessionReportGenerator


# Виджет для отображения одного показателя статистики
class StatCard(QWidget):

    def __init__(self, title: str, initial_value: str = "0", parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(4)

        self.label_title = CustomLabel(title, is_sub=True)
        self.label_value = QLabel(initial_value)
        self.label_value.setStyleSheet("font-size: 15px; font-weight: bold; color: #0f172a;")

        layout.addWidget(self.label_title)
        layout.addWidget(self.label_value)

        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
            }
        """)

    def set_value(self, text: str):
        self.label_value.setText(text)


# Главное окно программы
class InventoryAppWindow(CustomMainWindow):

    COLUMNS = ["ID", "Наименование", "Категория", "Цена", "Кол-во", "Штрихкод", "Рейтинг"]

    def __init__(self, username: str = "admin"):
        super().__init__()
        self._username = username
        self._time_in = datetime.now()
        self._repository = ProductRepository()

        # Маппинг столбцов и подсчета категорий
        self._column_mapping = CustomMap()
        self._category_stats_map = CustomMap()

        self._init_data()
        self._init_ui()
        self._refresh_table()

        # Привязываем сохранение отчета к закрытию окна
        self.exit_handler = self.save_session_report

    @property
    def username(self) -> str:
        return self._username

    @property
    def repository(self) -> ProductRepository:
        return self._repository

    def _init_data(self):
        # Заполняем маппинг колонок
        for idx, col in enumerate(self.COLUMNS):
            self._column_mapping.put(idx, col)

        # Загружаем товары на склад
        for prod in ProductRepository.create_initial_dataset():
            self._repository.add(prod)

    def _init_ui(self):
        self.setWindowTitle(f"Складской учёт - Пользователь: {self._username}")
        self.resize(1150, 720)
        self.setMinimumSize(900, 600)

        # Центральный виджет
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(14, 14, 14, 10)
        main_layout.setSpacing(10)

        # 1. Верхняя панель
        main_layout.addWidget(self._create_header_panel())

        # 2. Панель поиска и фильтрации
        main_layout.addWidget(self._create_filter_panel())

        # 3. Основная рабочая область (таблица + боковая панель)
        main_layout.addWidget(self._create_content_panel(), 1)

        # 4. Нижняя панель действий (кнопки)
        main_layout.addLayout(self._create_action_bar())

        # Строка состояния
        self.custom_status_bar = CustomStatusBar()
        self.setStatusBar(self.custom_status_bar)
        self.custom_status_bar.showMessage("Готово к работе")

    def _create_header_panel(self) -> QWidget:
        # Простая верхняя плашка с приветствием
        header = QWidget()
        header.setFixedHeight(48)
        header.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
            }
        """)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(14, 0, 14, 0)

        title = QLabel("Каталог складских запасов")
        title.setStyleSheet("font-size: 15px; font-weight: bold; color: #1e293b; border: none;")
        layout.addWidget(title)

        layout.addStretch()

        time_str = SessionReportGenerator.format_datetime(self._time_in)
        session_info = QLabel(f"Пользователь: <b>{self._username}</b> | Вход: {time_str}")
        session_info.setStyleSheet("font-size: 12px; color: #64748b; border: none;")
        layout.addWidget(session_info)

        return header

    def _create_filter_panel(self) -> CustomGroupBox:
        # Блок поиска и фильтрации товаров
        group = CustomGroupBox("Поиск и фильтры")

        grid = QGridLayout(group)
        grid.setContentsMargins(12, 14, 12, 12)
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(8)

        # Поиск
        grid.addWidget(CustomLabel("Поиск:", is_sub=True), 0, 0,
                       Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.search_input = CustomLineEdit("Поиск по наименованию, штрихкоду или описанию...")
        self.search_input.textChanged.connect(self._on_filter_changed)
        grid.addWidget(self.search_input, 0, 1)

        # Категория
        grid.addWidget(CustomLabel("Категория:", is_sub=True), 0, 2,
                       Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.combo_category = CustomComboBox()
        self.combo_category.addItem("Все категории")
        for cat in sorted(self._repository.get_unique_categories_as_set()):
            self.combo_category.addItem(cat)
        self.combo_category.currentTextChanged.connect(self._on_filter_changed)
        grid.addWidget(self.combo_category, 0, 3)

        # Чекбокс только в наличии
        self.check_in_stock = CustomCheckBox("Только товары в наличии")
        self.check_in_stock.stateChanged.connect(self._on_filter_changed)
        grid.addWidget(self.check_in_stock, 1, 1)

        # Кнопки сброса и сортировки
        btn_box = QHBoxLayout()
        btn_box.setSpacing(6)

        self.btn_reset = CustomButton("Сбросить")
        self.btn_reset.clicked.connect(self._reset_filters)
        btn_box.addWidget(self.btn_reset)

        self.btn_sort_price = CustomButton("По цене")
        self.btn_sort_price.clicked.connect(self._sort_by_price)
        btn_box.addWidget(self.btn_sort_price)

        self.btn_sort_id = CustomButton("По ID")
        self.btn_sort_id.clicked.connect(self._sort_by_id)
        btn_box.addWidget(self.btn_sort_id)

        grid.addLayout(btn_box, 1, 3)

        grid.setColumnStretch(1, 3)
        grid.setColumnStretch(3, 2)

        return group

    def _create_content_panel(self) -> QSplitter:
        # Разделитель: слева таблица, справа детали выбранного товара
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(8)

        # Таблица
        table_container = QWidget()
        t_layout = QVBoxLayout(table_container)
        t_layout.setContentsMargins(0, 0, 0, 0)

        self.table = CustomTableWidget(0, len(self.COLUMNS))
        self.table.setHorizontalHeaderLabels(self.COLUMNS)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)

        self.table.setSelectionBehavior(CustomTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(CustomTableWidget.SelectionMode.SingleSelection)
        self.table.itemSelectionChanged.connect(self._on_table_selection)
        self.table.delete_requested_signal.connect(self._delete_selected_product)
        self.table.doubleClicked.connect(self._edit_selected_product)

        t_layout.addWidget(self.table)
        splitter.addWidget(table_container)

        # Боковая панель
        side_panel = QWidget()
        side_panel.setMinimumWidth(280)
        side_panel.setMaximumWidth(350)
        s_layout = QVBoxLayout(side_panel)
        s_layout.setContentsMargins(0, 0, 0, 0)
        s_layout.setSpacing(10)

        s_layout.addWidget(self._create_details_box())
        s_layout.addWidget(self._create_stats_box())
        s_layout.addStretch()

        splitter.addWidget(side_panel)

        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)

        return splitter

    def _create_details_box(self) -> CustomGroupBox:
        # Карточка с информацией о выбранном товаре
        box = CustomGroupBox("Карточка товара")
        layout = QVBoxLayout(box)
        layout.setContentsMargins(12, 14, 12, 12)
        layout.setSpacing(6)

        self.label_item_title = QLabel("Выберите товар из таблицы")
        self.label_item_title.setWordWrap(True)
        self.label_item_title.setStyleSheet("font-size: 13px; font-weight: bold; color: #1e293b;")
        layout.addWidget(self.label_item_title)

        self.text_item_desc = CustomTextEdit("Здесь будет отображаться подробное описание...")
        self.text_item_desc.setReadOnly(True)
        self.text_item_desc.setMinimumHeight(110)
        self.text_item_desc.setMaximumHeight(160)
        layout.addWidget(self.text_item_desc)

        return box

    def _create_stats_box(self) -> CustomGroupBox:
        # Сводка статистики по складу
        box = CustomGroupBox("Статистика")
        layout = QVBoxLayout(box)
        layout.setContentsMargins(12, 14, 12, 12)
        layout.setSpacing(8)

        cards_row = QHBoxLayout()
        cards_row.setSpacing(6)
        self.card_total_items = StatCard("Позиций:")
        self.card_total_qty = StatCard("Штук на складе:")
        cards_row.addWidget(self.card_total_items)
        cards_row.addWidget(self.card_total_qty)
        layout.addLayout(cards_row)

        self.card_total_val = StatCard("Общая стоимость товаров:")
        layout.addWidget(self.card_total_val)

        layout.addWidget(CustomLabel("Заполнение склада:", is_sub=True))
        self.progress_stock = CustomProgressBar()
        layout.addWidget(self.progress_stock)

        self.label_categories = CustomLabel("", is_sub=True)
        self.label_categories.setWordWrap(True)
        layout.addWidget(self.label_categories)

        return box

    def _create_action_bar(self) -> QHBoxLayout:
        # Панель кнопок внизу окна
        layout = QHBoxLayout()
        layout.setSpacing(8)

        self.btn_add = CustomButton("Добавить товар", primary=True)
        self.btn_add.clicked.connect(self._add_product)
        layout.addWidget(self.btn_add)

        self.btn_edit = CustomButton("Редактировать")
        self.btn_edit.clicked.connect(self._edit_selected_product)
        layout.addWidget(self.btn_edit)

        self.btn_delete = CustomButton("Удалить", danger=True)
        self.btn_delete.clicked.connect(self._delete_selected_product)
        layout.addWidget(self.btn_delete)

        layout.addStretch()

        self.btn_report = CustomButton("Отчёт сессии")
        self.btn_report.clicked.connect(self._preview_report)
        layout.addWidget(self.btn_report)

        self.btn_exit = CustomButton("Выход")
        self.btn_exit.clicked.connect(self.close)
        layout.addWidget(self.btn_exit)

        return layout

    # Обновление данных в таблице
    def _refresh_table(self):
        products = ProductRepository.filter_products(
            self._repository.items,
            query=self.search_input.text(),
            category=self.combo_category.currentText(),
            in_stock_only=self.check_in_stock.isChecked(),
        )

        self.table.blockSignals(True)
        self.table.setRowCount(0)
        self.table.setRowCount(len(products))

        for row, prod in enumerate(products):
            row_data = prod.to_row()
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

                # Выравнивание чисел вправо
                if col in (0, 3, 4, 6):
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                else:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

                # Если нет в наличии, выделяем цветом
                if col == 4 and prod.quantity == 0:
                    item.setForeground(QColor("#94a3b8"))

                self.table.setItem(row, col, item)

        self.table.blockSignals(False)
        self._update_stats(products)
        self.custom_status_bar.showMessage(f"Отображается товаров: {len(products)} из {self._repository.count()}")

    def _update_stats(self, filtered_products: list):
        total_items = self._repository.count()
        total_qty = ProductRepository.calculate_total_quantity(self._repository.items)
        total_val = ProductRepository.calculate_total_value(self._repository.items)

        self.card_total_items.set_value(f"{total_items} шт.")
        self.card_total_qty.set_value(f"{total_qty} шт.")
        self.card_total_val.set_value(f"{total_val:,.2f} руб.")

        # Расчет заполненности относительно лимита в 300 штук
        limit = 300
        percent = min(100, int((total_qty / limit) * 100)) if limit > 0 else 0
        self.progress_stock.setValue(percent)
        self.progress_stock.setFormat(f"{percent}% ({total_qty} / {limit} шт.)")

        # Подсчет количества товаров по категориям через CustomMap
        self._category_stats_map.clear()
        for p in self._repository.items:
            current_count = self._category_stats_map.get(p.category, 0)
            self._category_stats_map.put(p.category, current_count + 1)

        cat_lines = list()
        for cat, cnt in self._category_stats_map.items():
            cat_lines.append(f"{cat}: {cnt}")
        self.label_categories.setText("  •  ".join(cat_lines))

    def _on_table_selection(self):
        selected = self.table.selectedItems()
        if not selected:
            self.label_item_title.setText("Выберите товар из таблицы")
            self.text_item_desc.setPlainText("")
            return

        row = self.table.currentRow()
        id_item = self.table.item(row, 0)
        if not id_item:
            return

        try:
            prod_id = int(id_item.text())
        except ValueError:
            return

        prod = self._repository.find_by_id(prod_id)
        if not prod:
            return

        self.label_item_title.setText(prod.name)

        stars = "★" * int(prod.rating)
        info_text = (
            f"Категория: {prod.category}\n"
            f"Цена: {prod.price:,.2f} руб.\n"
            f"Количество: {prod.quantity} шт."
            + (" (нет на складе)" if prod.quantity == 0 else "") + "\n"
            f"Штрихкод: {prod.barcode}\n"
            f"Оценка: {prod.rating} {stars}\n\n"
            f"Описание:\n{prod.description}"
        )
        self.text_item_desc.setPlainText(info_text)

    def _on_filter_changed(self):
        self._refresh_table()

    def _reset_filters(self):
        self.search_input.clear()
        self.combo_category.setCurrentIndex(0)
        self.check_in_stock.setChecked(False)

    def _sort_by_price(self):
        # Используем переопределенный __lt__
        self._repository.items.sort()
        self._refresh_table()
        self.custom_status_bar.showMessage("Товары отсортированы по цене")

    def _sort_by_id(self):
        self._repository.items.sort(key=lambda p: p.id)
        self._refresh_table()
        self.custom_status_bar.showMessage("Товары отсортированы по ID")

    def _add_product(self):
        dialog = ProductEditDialog(None, self)
        if dialog.exec():
            new_item = dialog.get_product()
            if self._repository.find_by_id(new_item.id):
                QMessageBox.warning(self, "Ошибка", f"Товар с ID {new_item.id} уже существует!")
                return

            self._repository.add(new_item)

            # Добавляем категорию в фильтр, если она новая
            if self.combo_category.findText(new_item.category) == -1:
                self.combo_category.addItem(new_item.category)

            self._refresh_table()
            self.custom_status_bar.showMessage(f"Добавлен товар: {new_item.name}")

    def _edit_selected_product(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Информация", "Выберите товар для редактирования")
            return

        id_item = self.table.item(row, 0)
        if not id_item:
            return

        prod = self._repository.find_by_id(int(id_item.text()))
        if not prod:
            return

        dialog = ProductEditDialog(prod, self)
        if dialog.exec():
            updated = dialog.get_product()
            prod.name = updated.name
            prod.category = updated.category
            prod.price = updated.price
            prod.quantity = updated.quantity
            prod.barcode = updated.barcode
            prod.rating = updated.rating
            prod.description = updated.description

            self._refresh_table()
            self._on_table_selection()
            self.custom_status_bar.showMessage(f"Товар '{prod.name}' успешно обновлен")

    def _delete_selected_product(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Информация", "Выберите товар для удаления")
            return

        id_item = self.table.item(row, 0)
        if not id_item:
            return

        prod = self._repository.find_by_id(int(id_item.text()))
        if not prod:
            return

        reply = QMessageBox.question(
            self, "Подтверждение",
            f"Удалить товар '{prod.name}' со склада?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self._repository.remove_by_id(prod.id)
            self._refresh_table()
            self.custom_status_bar.showMessage(f"Удален товар: {prod.name}")

    def _preview_report(self):
        record = SessionRecord(self._username, self._time_in, datetime.now())
        report_text = SessionReportGenerator.build_report_table(record)
        QMessageBox.information(
            self, "Отчёт сессии",
            f"Текущая сессия:\n\n{report_text}\n\nОтчёт автоматически сохранится при выходе."
        )

    def save_session_report(self):
        # Метод сохранения отчета в файл session_report.txt при выходе
        record = SessionRecord(self._username, self._time_in, datetime.now())
        SessionReportGenerator.save_report_to_file(record, "session_report.txt")
