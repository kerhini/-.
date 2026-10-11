"""Главное окно приложения складского учёта."""

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
    QFrame,
    QSizePolicy,
    QLabel,
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QColor

from custom_map import CustomMap
from entities import Product, ProductRepository
from custom_widgets import (
    CustomMainWindow,
    CustomButton,
    CustomLineEdit,
    CustomLabel,
    CustomTableWidget,
    CustomComboBox,
    CustomSpinBox,
    CustomCheckBox,
    CustomProgressBar,
    CustomTextEdit,
    CustomGroupBox,
    CustomStatusBar,
    # Цветовые константы
    _BG_APP, _BG_CARD, _BG_ROW, _BORDER, _ACCENT, _ACCENT_LIGHT,
    _TEXT_H, _TEXT_B, _TEXT_SUB, _RED,
)
from product_dialog import ProductEditDialog
from report_generator import SessionRecord, SessionReportGenerator


# ─── Вспомогательный горизонтальный разделитель ──────────────────────────────
class _HDivider(QFrame):
    """Тонкая горизонтальная линия-разделитель."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFixedHeight(1)
        self.setStyleSheet(f"background-color: {_BORDER}; border: none;")


class _StatCard(QWidget):
    """Карточка одного показателя аналитики."""

    def __init__(self, label: str, value: str = "—", accent: bool = False, parent=None):
        super().__init__(parent)
        self._lbl_title = CustomLabel(label, is_sub=True)
        self._lbl_value = CustomLabel(value, is_title=accent)
        if not accent:
            self._lbl_value.setStyleSheet(
                f"font-size: 16px; font-weight: 700; color: {_TEXT_H};"
            )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(2)
        layout.addWidget(self._lbl_title)
        layout.addWidget(self._lbl_value)

        border_color = _ACCENT if accent else _BORDER
        self.setStyleSheet(
            f"QWidget {{"
            f"  background: {_BG_CARD};"
            f"  border: 1px solid {border_color};"
            f"  border-radius: 10px;"
            f"}}"
        )

    def set_value(self, text: str):
        """Обновить отображаемое значение карточки."""
        self._lbl_value.setText(text)


# ─── Главное окно ─────────────────────────────────────────────────────────────
class InventoryAppWindow(CustomMainWindow):
    """Главное окно системы складского учёта."""

    # Заголовки колонок таблицы
    _COL_HEADERS = ["ID", "Наименование", "Категория", "Цена", "Кол-во", "Штрихкод", "Рейтинг"]
    # Ширины колонок: True = Stretch, False = ResizeToContents
    _COL_STRETCH  = [False, True,  True,  False, False, False, False]

    def __init__(self, username: str = "Admin"):
        super().__init__()
        self._username = username
        self._time_in  = datetime.now()
        self._repository = ProductRepository()

        self._column_mapping     = CustomMap()
        self._category_stats_map = CustomMap()

        self._setup_column_mapping()
        self._init_repository()
        self._setup_ui()
        self._refresh_table()

        self.exit_handler = self.save_session_report

    # ── свойства ─────────────────────────────────────────────────────────────

    @property
    def username(self) -> str:
        return self._username

    @property
    def repository(self) -> ProductRepository:
        return self._repository

    # ── инициализация ─────────────────────────────────────────────────────────

    def _setup_column_mapping(self):
        """Маппинг индекс → заголовок через CustomMap (без dict)."""
        for idx, header in enumerate(self._COL_HEADERS):
            self._column_mapping.put(idx, header)

    def _init_repository(self):
        """Загрузка начального каталога: >= 10 объектов Product."""
        for prod in ProductRepository.create_initial_dataset():
            self._repository.add(prod)

    # ── построение UI ─────────────────────────────────────────────────────────

    def _setup_ui(self):
        self.setWindowTitle(
            f"Складской учёт — {self._username}"
        )
        self.resize(1200, 760)
        self.setMinimumSize(900, 600)

        # Глобальный фон и шрифт
        self.setStyleSheet(
            f"QMainWindow, QWidget#root {{ background-color: {_BG_APP}; }}"
            f"* {{ font-family: 'Segoe UI', 'Arial', sans-serif; }}"
        )

        root = QWidget(self)
        root.setObjectName("root")
        self.setCentralWidget(root)

        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # ── Шапка ──────────────────────────────────────────────────────────
        root_layout.addWidget(self._build_header())
        root_layout.addWidget(_HDivider())

        # ── Тело (панель фильтров + контент) ───────────────────────────────
        body = QWidget()
        body.setStyleSheet(f"background: {_BG_APP};")
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(16, 14, 16, 12)
        body_layout.setSpacing(12)

        body_layout.addWidget(self._build_filter_bar())
        body_layout.addWidget(self._build_content_splitter(), 1)
        body_layout.addWidget(_HDivider())
        body_layout.addLayout(self._build_action_bar())

        root_layout.addWidget(body, 1)

        # ── Строка состояния ───────────────────────────────────────────────
        self.custom_status_bar = CustomStatusBar()
        self.setStatusBar(self.custom_status_bar)
        self.custom_status_bar.showMessage("Система готова к работе")

    def _build_header(self) -> QWidget:
        """Шапка приложения: логотип-иконка, заголовок, информация о сессии."""
        header = QWidget()
        header.setFixedHeight(62)
        header.setStyleSheet(
            f"background: {_BG_CARD}; border-bottom: 1px solid {_BORDER};"
        )
        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(12)

        # Цветной прямоугольник-«иконка»
        badge = QLabel("SKU")
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setFixedSize(44, 34)
        badge.setStyleSheet(
            f"background: {_ACCENT}; color: #fff;"
            f"border-radius: 8px; font-size: 13px; font-weight: 800;"
            f"letter-spacing: 1px;"
        )
        layout.addWidget(badge)

        # Заголовок
        title = QLabel("Складской учёт")
        title.setStyleSheet(
            f"font-size: 16px; font-weight: 700; color: {_TEXT_H};"
        )
        layout.addWidget(title)

        layout.addStretch()

        # Информация о сессии
        session_text = (
            f"Пользователь: <b>{self._username}</b> &nbsp;|&nbsp; "
            f"Вход: {SessionReportGenerator.format_datetime(self._time_in)}"
        )
        self.label_session_info = QLabel(session_text)
        self.label_session_info.setStyleSheet(
            f"font-size: 12px; color: {_TEXT_SUB};"
        )
        self.label_session_info.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(self.label_session_info)

        return header

    def _build_filter_bar(self) -> CustomGroupBox:
        """Панель поиска и фильтрации."""
        group = CustomGroupBox("Поиск и фильтрация")

        grid = QGridLayout(group)
        grid.setContentsMargins(14, 18, 14, 14)
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(10)

        # Строка 0: Поиск | Метка | Категория | Метка
        grid.addWidget(CustomLabel("Поиск:", is_sub=True), 0, 0,
                       Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.search_input = CustomLineEdit(
            "Поиск по наименованию, штрихкоду или описанию..."
        )
        self.search_input.textChanged.connect(self._on_filter_changed)
        grid.addWidget(self.search_input, 0, 1)

        grid.addWidget(CustomLabel("Категория:", is_sub=True), 0, 2,
                       Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.combo_category = CustomComboBox()
        self.combo_category.addItem("Все категории")
        for cat in sorted(self._repository.get_unique_categories_as_set()):
            self.combo_category.addItem(cat)
        self.combo_category.currentTextChanged.connect(self._on_filter_changed)
        grid.addWidget(self.combo_category, 0, 3)

        # Строка 1: Чекбокс | Кнопки
        self.check_in_stock = CustomCheckBox("Только товары в наличии")
        self.check_in_stock.stateChanged.connect(self._on_filter_changed)
        grid.addWidget(self.check_in_stock, 1, 1)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        self.btn_reset_filters = CustomButton("Сбросить")
        self.btn_reset_filters.clicked.connect(self._reset_filters)
        btn_row.addWidget(self.btn_reset_filters)

        self.btn_sort_price = CustomButton("По цене ▲")
        self.btn_sort_price.clicked.connect(self._sort_by_price)
        btn_row.addWidget(self.btn_sort_price)

        self.btn_sort_id = CustomButton("По ID")
        self.btn_sort_id.clicked.connect(self._sort_by_id)
        btn_row.addWidget(self.btn_sort_id)

        grid.addLayout(btn_row, 1, 3)

        grid.setColumnStretch(1, 3)
        grid.setColumnStretch(3, 2)

        return group

    def _build_content_splitter(self) -> QSplitter:
        """Сплиттер: таблица слева, панель деталей справа."""
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(10)
        splitter.setStyleSheet(
            "QSplitter::handle { background: transparent; }"
        )

        # ─ Левая: таблица ──────────────────────────────────────────────────
        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)

        col_count = len(self._COL_HEADERS)
        self.table = CustomTableWidget(0, col_count)
        self.table.setHorizontalHeaderLabels(self._COL_HEADERS)

        hh = self.table.horizontalHeader()
        for col, stretch in enumerate(self._COL_STRETCH):
            if stretch:
                hh.setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)
            else:
                hh.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)

        self.table.setSelectionBehavior(CustomTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(CustomTableWidget.SelectionMode.SingleSelection)
        self.table.itemSelectionChanged.connect(self._on_selection_changed)
        self.table.delete_requested_signal.connect(self._delete_selected_product)
        self.table.doubleClicked.connect(self._edit_selected_product)

        left_layout.addWidget(self.table)
        splitter.addWidget(left)

        # ─ Правая: детали + аналитика ──────────────────────────────────────
        right = QWidget()
        right.setMinimumWidth(260)
        right.setMaximumWidth(340)
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(12)

        right_layout.addWidget(self._build_details_panel())
        right_layout.addWidget(self._build_analytics_panel())
        right_layout.addStretch()

        splitter.addWidget(right)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 0)

        return splitter

    def _build_details_panel(self) -> CustomGroupBox:
        """Карточка выбранного товара."""
        group = CustomGroupBox("Карточка товара")
        layout = QVBoxLayout(group)
        layout.setContentsMargins(14, 18, 14, 14)
        layout.setSpacing(8)

        self.label_selected_title = QLabel("Выберите товар")
        self.label_selected_title.setWordWrap(True)
        self.label_selected_title.setStyleSheet(
            f"font-size: 14px; font-weight: 700; color: {_TEXT_H};"
        )
        layout.addWidget(self.label_selected_title)

        self.text_description = CustomTextEdit("Описание появится здесь...")
        self.text_description.setReadOnly(True)
        self.text_description.setMinimumHeight(120)
        self.text_description.setMaximumHeight(200)
        layout.addWidget(self.text_description)

        return group

    def _build_analytics_panel(self) -> CustomGroupBox:
        """Панель складской аналитики."""
        group = CustomGroupBox("Аналитика")
        layout = QVBoxLayout(group)
        layout.setContentsMargins(14, 18, 14, 14)
        layout.setSpacing(10)

        # Три карточки с показателями
        cards_row1 = QHBoxLayout()
        cards_row1.setSpacing(8)
        self.card_count = _StatCard("Наименований", "0 шт.")
        self.card_units = _StatCard("Единиц на складе", "0 шт.")
        cards_row1.addWidget(self.card_count)
        cards_row1.addWidget(self.card_units)
        layout.addLayout(cards_row1)

        self.card_cost = _StatCard("Общая стоимость", "0.00 руб.", accent=True)
        layout.addWidget(self.card_cost)

        # Полоса заполненности
        self.label_capacity = CustomLabel("Заполненность склада:", is_sub=True)
        layout.addWidget(self.label_capacity)

        self.progress_capacity = CustomProgressBar()
        layout.addWidget(self.progress_capacity)

        # Разбивка по категориям
        self.label_category_breakdown = CustomLabel("", is_sub=True)
        self.label_category_breakdown.setWordWrap(True)
        layout.addWidget(self.label_category_breakdown)

        return group

    def _build_action_bar(self) -> QHBoxLayout:
        """Нижняя панель действий с кнопками CRUD."""
        layout = QHBoxLayout()
        layout.setSpacing(8)

        self.btn_add = CustomButton("+ Добавить", primary=True)
        self.btn_add.clicked.connect(self._add_product)
        layout.addWidget(self.btn_add)

        self.btn_edit = CustomButton("Редактировать")
        self.btn_edit.clicked.connect(self._edit_selected_product)
        layout.addWidget(self.btn_edit)

        self.btn_delete = CustomButton("Удалить", danger=True)
        self.btn_delete.clicked.connect(self._delete_selected_product)
        layout.addWidget(self.btn_delete)

        layout.addStretch()

        self.btn_report_preview = CustomButton("Предпросмотр отчёта")
        self.btn_report_preview.clicked.connect(self._show_session_report_preview)
        layout.addWidget(self.btn_report_preview)

        self.btn_exit = CustomButton("Выход")
        self.btn_exit.clicked.connect(self.close)
        layout.addWidget(self.btn_exit)

        return layout

    # ── логика таблицы и данных ───────────────────────────────────────────────

    def _get_current_filtered_products(self) -> list:
        """Получить список отфильтрованных товаров (@staticmethod ProductRepository)."""
        return ProductRepository.filter_products(
            self._repository.items,
            query=self.search_input.text(),
            category=self.combo_category.currentText(),
            in_stock_only=self.check_in_stock.isChecked(),
        )

    def _refresh_table(self):
        """Полная перерисовка таблицы товаров."""
        products = self._get_current_filtered_products()

        # Блокируем сигналы, чтобы не триггерить selection_changed во время заполнения
        self.table.blockSignals(True)
        self.table.setRowCount(0)
        self.table.setRowCount(len(products))

        for row_idx, product in enumerate(products):
            row_data = product.to_row()   # возвращает 7 значений
            for col_idx, cell_value in enumerate(row_data):
                item = QTableWidgetItem(str(cell_value))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                # Числовые колонки — по правому краю, текстовые — по левому
                if col_idx in (0, 3, 4, 6):
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                    )
                else:
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
                    )
                # Подсветка: нет в наличии → серый текст
                if col_idx == 4 and product.quantity == 0:
                    item.setForeground(QColor("#94a3b8"))
                self.table.setItem(row_idx, col_idx, item)

        self.table.blockSignals(False)
        self._update_analytics(products)
        self.custom_status_bar.showMessage(
            f"Показано {len(products)} из {self._repository.count()} товаров"
        )

    def _update_analytics(self, _current_products: list):
        """Пересчёт аналитики склада с использованием CustomMap."""
        total_count = self._repository.count()
        total_units = ProductRepository.calculate_total_quantity(self._repository.items)
        total_cost  = ProductRepository.calculate_total_value(self._repository.items)

        self.card_count.set_value(f"{total_count} шт.")
        self.card_units.set_value(f"{total_units} шт.")
        self.card_cost.set_value(f"{total_cost:,.2f} руб.")

        max_quota  = 300
        percentage = min(100, int(total_units / max_quota * 100)) if max_quota else 0
        self.progress_capacity.setValue(percentage)
        self.progress_capacity.setFormat(
            f"{percentage}%  ({total_units} / {max_quota} шт.)"
        )

        # Подсчёт по категориям через CustomMap (без dict)
        self._category_stats_map.clear()
        for p in self._repository.items:
            cnt = self._category_stats_map.get(p.category, 0)
            self._category_stats_map.put(p.category, cnt + 1)

        parts = list()
        for cat, cnt in self._category_stats_map.items():
            parts.append(f"{cat}: {cnt}")
        self.label_category_breakdown.setText("  •  ".join(parts))

    def _on_selection_changed(self):
        """Показ детальной карточки выбранного товара."""
        selected = self.table.selectedItems()
        if not selected:
            self.label_selected_title.setText("Выберите товар")
            self.text_description.setPlainText("")
            return

        row_idx = self.table.currentRow()
        id_item = self.table.item(row_idx, 0)
        if not id_item:
            return

        try:
            product_id = int(id_item.text())
        except ValueError:
            return

        product = self._repository.find_by_id(product_id)
        if not product:
            return

        self.label_selected_title.setText(product.name)

        stars = "★" * int(product.rating) + "☆" * (5 - int(product.rating))
        desc = (
            f"Рейтинг: {stars}  {product.rating}\n"
            f"Категория: {product.category}\n"
            f"Цена: {product.price:,.2f} руб.\n"
            f"На складе: {product.quantity} шт."
            + (" [НЕТ В НАЛИЧИИ]" if product.quantity == 0 else "") + "\n"
            f"Штрихкод: {product.barcode}\n\n"
            f"{product.description}"
        )
        self.text_description.setPlainText(desc)

    # ── обработчики действий ──────────────────────────────────────────────────

    def _on_filter_changed(self):
        self._refresh_table()

    def _reset_filters(self):
        self.search_input.clear()
        self.combo_category.setCurrentIndex(0)
        self.check_in_stock.setChecked(False)

    def _sort_by_price(self):
        """Сортировка по цене — использует переопределённый __lt__ в Product."""
        self._repository.items.sort()
        self._refresh_table()
        self.custom_status_bar.showMessage(
            "Сортировка по цене (переопределённый __lt__)"
        )

    def _sort_by_id(self):
        self._repository.items.sort(key=lambda p: p.id)
        self._refresh_table()
        self.custom_status_bar.showMessage("Сортировка по ID")

    def _add_product(self):
        dialog = ProductEditDialog(None, self)
        if dialog.exec():
            new_prod = dialog.get_product()
            if self._repository.find_by_id(new_prod.id):
                QMessageBox.warning(
                    self, "Ошибка",
                    f"Товар с ID {new_prod.id} уже существует!"
                )
                return
            self._repository.add(new_prod)
            if self.combo_category.findText(new_prod.category) == -1:
                self.combo_category.addItem(new_prod.category)
            self._refresh_table()
            self.custom_status_bar.showMessage(f"Добавлен: {new_prod.name}")

    def _edit_selected_product(self):
        row_idx = self.table.currentRow()
        if row_idx < 0:
            QMessageBox.information(self, "Внимание", "Выберите товар для редактирования")
            return

        id_item = self.table.item(row_idx, 0)
        if not id_item:
            return
        product = self._repository.find_by_id(int(id_item.text()))
        if not product:
            return

        dialog = ProductEditDialog(product, self)
        if dialog.exec():
            updated = dialog.get_product()
            product.name        = updated.name
            product.category    = updated.category
            product.price       = updated.price
            product.quantity    = updated.quantity
            product.barcode     = updated.barcode
            product.rating      = updated.rating
            product.description = updated.description
            self._refresh_table()
            self._on_selection_changed()
            self.custom_status_bar.showMessage(f"Обновлён товар №{product.id}")

    def _delete_selected_product(self):
        row_idx = self.table.currentRow()
        if row_idx < 0:
            QMessageBox.information(self, "Внимание", "Выберите товар для удаления")
            return

        id_item = self.table.item(row_idx, 0)
        if not id_item:
            return
        product = self._repository.find_by_id(int(id_item.text()))
        if not product:
            return

        confirm = QMessageBox.question(
            self, "Подтверждение удаления",
            f"Удалить товар «{product.name}» (ID: {product.id})?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm == QMessageBox.StandardButton.Yes:
            self._repository.remove_by_id(product.id)
            self._refresh_table()
            self.custom_status_bar.showMessage(f"Удалён: {product.name}")

    def _show_session_report_preview(self):
        record = SessionRecord(self._username, self._time_in, datetime.now())
        report_text = SessionReportGenerator.build_report_table(record)
        QMessageBox.information(
            self, "Предпросмотр отчёта сессии",
            f"Файл session_report.txt при выходе:\n\n{report_text}",
        )

    def save_session_report(self):
        """Сохранение отчёта при закрытии окна (вызывается из closeEvent)."""
        record = SessionRecord(self._username, self._time_in, datetime.now())
        saved  = SessionReportGenerator.save_report_to_file(record, "session_report.txt")
        print("\n--- ОТЧЁТ СЕССИИ СОХРАНЁН ---")
        print(saved)
        print("----------------------------\n")
