from PyQt6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QLineEdit,
    QLabel,
    QTableWidget,
    QComboBox,
    QDoubleSpinBox,
    QCheckBox,
    QProgressBar,
    QTextEdit,
    QGroupBox,
    QStatusBar,
    QDialog,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QKeyEvent, QPaintEvent, QMouseEvent


# 1. Кастомное главное окно
class CustomMainWindow(QMainWindow):

    window_closed_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._exit_handler = None
        self.setStyleSheet("QMainWindow { background-color: #f8fafc; }")

    @property
    def exit_handler(self):
        return self._exit_handler

    @exit_handler.setter
    def exit_handler(self, handler):
        self._exit_handler = handler

    # Переопределяем закрытие окна для сохранения отчета
    def closeEvent(self, event):
        if self._exit_handler is not None:
            self._exit_handler()
        self.window_closed_signal.emit()
        event.accept()

    # Переопределяем нажатие клавиш (Escape не закрывает окно)
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            event.ignore()
        else:
            super().keyPressEvent(event)


# 2. Кастомная кнопка
class CustomButton(QPushButton):

    def __init__(self, text: str = "", primary: bool = False,
                 danger: bool = False, parent=None):
        super().__init__(text, parent)
        self._primary = primary
        self._danger = danger
        self._apply_style()

    @property
    def is_primary(self) -> bool:
        return self._primary

    @is_primary.setter
    def is_primary(self, val: bool):
        self._primary = bool(val)
        self._apply_style()

    @staticmethod
    def get_primary_style() -> str:
        return """
            QPushButton {
                background-color: #2563eb;
                color: #ffffff;
                font-size: 13px;
                font-weight: bold;
                border-radius: 6px;
                padding: 7px 16px;
                border: none;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
            QPushButton:pressed {
                background-color: #1e40af;
            }
        """

    @staticmethod
    def get_secondary_style() -> str:
        return """
            QPushButton {
                background-color: #ffffff;
                color: #334155;
                font-size: 13px;
                border-radius: 6px;
                padding: 7px 14px;
                border: 1px solid #cbd5e1;
            }
            QPushButton:hover {
                background-color: #f1f5f9;
                border-color: #94a3b8;
            }
            QPushButton:pressed {
                background-color: #e2e8f0;
            }
        """

    @staticmethod
    def get_danger_style() -> str:
        return """
            QPushButton {
                background-color: #ffffff;
                color: #dc2626;
                font-size: 13px;
                border-radius: 6px;
                padding: 7px 14px;
                border: 1px solid #fca5a5;
            }
            QPushButton:hover {
                background-color: #fef2f2;
                border-color: #dc2626;
            }
            QPushButton:pressed {
                background-color: #fee2e2;
            }
        """

    def _apply_style(self):
        if self._danger:
            self.setStyleSheet(CustomButton.get_danger_style())
        elif self._primary:
            self.setStyleSheet(CustomButton.get_primary_style())
        else:
            self.setStyleSheet(CustomButton.get_secondary_style())

    # Меняем курсор мыши при наведении
    def enterEvent(self, event):
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)


# 3. Кастомное поле ввода текста
class CustomLineEdit(QLineEdit):

    enter_pressed_signal = pyqtSignal()

    def __init__(self, placeholder: str = "", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff;
                color: #1e293b;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #2563eb;
                background-color: #ffffff;
            }
        """)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.enter_pressed_signal.emit()
        super().keyPressEvent(event)


# 4. Кастомная текстовая метка
class CustomLabel(QLabel):

    def __init__(self, text: str = "", is_title: bool = False,
                 is_sub: bool = False, parent=None):
        super().__init__(text, parent)
        if is_title:
            self.setStyleSheet("font-size: 15px; font-weight: bold; color: #0f172a;")
        elif is_sub:
            self.setStyleSheet("font-size: 12px; color: #64748b;")
        else:
            self.setStyleSheet("font-size: 13px; color: #334155;")

    # Переопределяем отрисовку для демонстрации полиморфизма
    def paintEvent(self, event: QPaintEvent):
        super().paintEvent(event)


# 5. Кастомная таблица для каталога товаров
class CustomTableWidget(QTableWidget):

    delete_requested_signal = pyqtSignal()

    def __init__(self, rows: int = 0, columns: int = 0, parent=None):
        super().__init__(rows, columns, parent)

        # Прячем вертикальную нумерацию строк для аккуратного вида
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(38)
        self.setShowGrid(True)
        self.setAlternatingRowColors(True)

        self.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                alternate-background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                gridline-color: #f1f5f9;
                font-size: 13px;
                color: #334155;
            }
            QTableWidget::item {
                padding: 5px 8px;
            }
            QTableWidget::item:selected {
                background-color: #dbeafe;
                color: #1e3a8a;
            }
            QHeaderView::section {
                background-color: #f1f5f9;
                color: #475569;
                font-weight: bold;
                font-size: 12px;
                padding: 8px 6px;
                border: none;
                border-bottom: 1px solid #cbd5e1;
            }
        """)

    # Удаление товара по кнопке Delete на клавиатуре
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Delete:
            self.delete_requested_signal.emit()
        else:
            super().keyPressEvent(event)


# 6. Кастомный выпадающий список
class CustomComboBox(QComboBox):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QComboBox {
                background-color: #ffffff;
                color: #1e293b;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 13px;
                min-width: 140px;
            }
            QComboBox:focus {
                border: 1px solid #2563eb;
            }
            QComboBox QAbstractItemView {
                background-color: #ffffff;
                color: #1e293b;
                border: 1px solid #cbd5e1;
                selection-background-color: #dbeafe;
                selection-color: #1e3a8a;
            }
        """)

    def wheelEvent(self, event):
        # Отключаем скролл колесиком, чтобы случайно не сбить выбор
        event.ignore()


# 7. Кастомное поле для ввода чисел
class CustomSpinBox(QDoubleSpinBox):

    def __init__(self, minimum: float = 0.0, maximum: float = 1000000.0,
                 step: float = 1.0, parent=None):
        super().__init__(parent)
        self.setRange(minimum, maximum)
        self.setSingleStep(step)
        self.setStyleSheet("""
            QDoubleSpinBox {
                background-color: #ffffff;
                color: #1e293b;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 13px;
            }
            QDoubleSpinBox:focus {
                border: 1px solid #2563eb;
            }
        """)

    def keyPressEvent(self, event: QKeyEvent):
        super().keyPressEvent(event)


# 8. Кастомный чекбокс
class CustomCheckBox(QCheckBox):

    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QCheckBox {
                font-size: 13px;
                color: #334155;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border-radius: 4px;
                border: 1px solid #cbd5e1;
                background-color: #ffffff;
            }
            QCheckBox::indicator:checked {
                background-color: #2563eb;
                border-color: #2563eb;
            }
        """)

    def enterEvent(self, event):
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().leaveEvent(event)


# 9. Кастомный прогресс-бар
class CustomProgressBar(QProgressBar):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRange(0, 100)
        self.setValue(0)
        self.setTextVisible(True)
        self.setFixedHeight(18)
        self.setStyleSheet("""
            QProgressBar {
                background-color: #e2e8f0;
                border-radius: 6px;
                text-align: center;
                color: #0f172a;
                font-size: 11px;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #2563eb;
                border-radius: 6px;
            }
        """)

    def paintEvent(self, event: QPaintEvent):
        super().paintEvent(event)


# 10. Кастомное многострочное поле описания
class CustomTextEdit(QTextEdit):

    def __init__(self, placeholder: str = "", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setStyleSheet("""
            QTextEdit {
                background-color: #ffffff;
                color: #334155;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                padding: 8px;
                font-size: 13px;
            }
            QTextEdit:focus {
                border: 1px solid #2563eb;
            }
        """)

    def keyPressEvent(self, event: QKeyEvent):
        super().keyPressEvent(event)


# 11. Кастомная рамка с заголовком
class CustomGroupBox(QGroupBox):

    def __init__(self, title: str = "", parent=None):
        super().__init__(title, parent)
        self.setStyleSheet("""
            QGroupBox {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                margin-top: 14px;
                font-weight: bold;
                font-size: 13px;
                color: #0f172a;
                padding-top: 8px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 4px;
            }
        """)

    def paintEvent(self, event: QPaintEvent):
        super().paintEvent(event)


# 12. Кастомная строка состояния
class CustomStatusBar(QStatusBar):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QStatusBar {
                background-color: #ffffff;
                color: #64748b;
                border-top: 1px solid #e2e8f0;
                font-size: 12px;
                padding: 4px 10px;
            }
        """)

    def showMessage(self, message: str, timeout: int = 0):
        super().showMessage(f"  {message}", timeout)


# 13. Кастомное диалоговое окно
class CustomDialog(QDialog):

    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
            }
            QLabel {
                font-size: 13px;
                color: #334155;
            }
        """)

    def keyPressEvent(self, event: QKeyEvent):
        # Escape закрывает модальное окно с отменой
        if event.key() == Qt.Key.Key_Escape:
            self.reject()
        else:
            super().keyPressEvent(event)
