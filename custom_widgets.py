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
from PyQt6.QtGui import QKeyEvent, QPaintEvent


# 1. Главное окно программы с обработкой закрытия
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

    # Сохраняем отчет при закрытии окна
    def closeEvent(self, event):
        if self._exit_handler is not None:
            self._exit_handler()
        self.window_closed_signal.emit()
        event.accept()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            event.ignore()
        else:
            super().keyPressEvent(event)


# 2. Кнопка с подсветкой и простыми стилями
class CustomButton(QPushButton):

    def __init__(self, text="", primary=False, danger=False, parent=None):
        super().__init__(text, parent)
        self._primary = primary
        self._danger = danger
        self._apply_style()

    @property
    def is_primary(self):
        return self._primary

    @is_primary.setter
    def is_primary(self, val):
        self._primary = bool(val)
        self._apply_style()

    def _apply_style(self):
        if self._danger:
            self.setStyleSheet(
                "QPushButton { background-color: #dc2626; color: white; border-radius: 5px; padding: 6px 14px; font-weight: bold; border: none; }"
                "QPushButton:hover { background-color: #b91c1c; }"
            )
        elif self._primary:
            self.setStyleSheet(
                "QPushButton { background-color: #2563eb; color: white; border-radius: 5px; padding: 6px 14px; font-weight: bold; border: none; }"
                "QPushButton:hover { background-color: #1d4ed8; }"
            )
        else:
            self.setStyleSheet(
                "QPushButton { background-color: #ffffff; color: #334155; border: 1px solid #cbd5e1; border-radius: 5px; padding: 6px 12px; }"
                "QPushButton:hover { background-color: #f1f5f9; border-color: #94a3b8; }"
            )

    def enterEvent(self, event):
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().leaveEvent(event)


# 3. Текстовое поле ввода
class CustomLineEdit(QLineEdit):

    enter_pressed_signal = pyqtSignal()

    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setStyleSheet(
            "QLineEdit { background-color: #ffffff; color: #1e293b; border: 1px solid #cbd5e1; border-radius: 5px; padding: 6px 8px; font-size: 13px; }"
            "QLineEdit:focus { border: 1px solid #2563eb; }"
        )

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.enter_pressed_signal.emit()
        super().keyPressEvent(event)


# 4. Текстовая метка (заголовок или подпись)
class CustomLabel(QLabel):

    def __init__(self, text="", is_title=False, is_sub=False, parent=None):
        super().__init__(text, parent)
        if is_title:
            self.setStyleSheet("font-size: 15px; font-weight: bold; color: #0f172a;")
        elif is_sub:
            self.setStyleSheet("font-size: 12px; color: #64748b;")
        else:
            self.setStyleSheet("font-size: 13px; color: #334155;")

    def paintEvent(self, event: QPaintEvent):
        super().paintEvent(event)


# 5. Таблица товаров
class CustomTableWidget(QTableWidget):

    delete_requested_signal = pyqtSignal()

    def __init__(self, rows=0, columns=0, parent=None):
        super().__init__(rows, columns, parent)
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(36)
        self.setShowGrid(True)
        self.setAlternatingRowColors(True)
        self.setStyleSheet(
            "QTableWidget { background-color: #ffffff; alternate-background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; gridline-color: #f1f5f9; font-size: 13px; color: #334155; }"
            "QTableWidget::item:selected { background-color: #dbeafe; color: #1e3a8a; }"
            "QHeaderView::section { background-color: #f1f5f9; color: #475569; font-weight: bold; font-size: 12px; padding: 6px; border: none; border-bottom: 1px solid #cbd5e1; }"
        )

    # Удаление товара при нажатии Delete
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Delete:
            self.delete_requested_signal.emit()
        else:
            super().keyPressEvent(event)


# 6. Выпадающий список выбора категории
class CustomComboBox(QComboBox):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            "QComboBox { background-color: #ffffff; color: #1e293b; border: 1px solid #cbd5e1; border-radius: 5px; padding: 5px 8px; font-size: 13px; min-width: 130px; }"
            "QComboBox:focus { border: 1px solid #2563eb; }"
        )

    def wheelEvent(self, event):
        # Игнорируем колесико мыши, чтобы случайно не переключить
        event.ignore()


# 7. Поле для ввода чисел
class CustomSpinBox(QDoubleSpinBox):

    def __init__(self, minimum=0.0, maximum=1000000.0, step=1.0, parent=None):
        super().__init__(parent)
        self.setRange(minimum, maximum)
        self.setSingleStep(step)
        self.setStyleSheet(
            "QDoubleSpinBox { background-color: #ffffff; color: #1e293b; border: 1px solid #cbd5e1; border-radius: 5px; padding: 5px 8px; font-size: 13px; }"
            "QDoubleSpinBox:focus { border: 1px solid #2563eb; }"
        )

    def keyPressEvent(self, event: QKeyEvent):
        super().keyPressEvent(event)


# 8. Чекбокс фильтрации
class CustomCheckBox(QCheckBox):

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(
            "QCheckBox { font-size: 13px; color: #334155; spacing: 6px; }"
            "QCheckBox::indicator { width: 16px; height: 16px; border-radius: 3px; border: 1px solid #cbd5e1; background-color: #ffffff; }"
            "QCheckBox::indicator:checked { background-color: #2563eb; border-color: #2563eb; }"
        )

    def enterEvent(self, event):
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().leaveEvent(event)


# 9. Индикатор заполненности склада
class CustomProgressBar(QProgressBar):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRange(0, 100)
        self.setValue(0)
        self.setTextVisible(True)
        self.setFixedHeight(18)
        self.setStyleSheet(
            "QProgressBar { background-color: #e2e8f0; border-radius: 4px; text-align: center; color: #0f172a; font-size: 11px; font-weight: bold; }"
            "QProgressBar::chunk { background-color: #2563eb; border-radius: 4px; }"
        )

    def paintEvent(self, event: QPaintEvent):
        super().paintEvent(event)


# 10. Многострочное текстовое поле описания
class CustomTextEdit(QTextEdit):

    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setStyleSheet(
            "QTextEdit { background-color: #ffffff; color: #334155; border: 1px solid #cbd5e1; border-radius: 5px; padding: 6px; font-size: 13px; }"
            "QTextEdit:focus { border: 1px solid #2563eb; }"
        )

    def keyPressEvent(self, event: QKeyEvent):
        super().keyPressEvent(event)


# 11. Группа с рамкой и заголовком
class CustomGroupBox(QGroupBox):

    def __init__(self, title="", parent=None):
        super().__init__(title, parent)
        self.setStyleSheet(
            "QGroupBox { background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; margin-top: 12px; font-weight: bold; font-size: 13px; color: #0f172a; padding-top: 8px; }"
            "QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 4px; }"
        )

    def paintEvent(self, event: QPaintEvent):
        super().paintEvent(event)


# 12. Строка состояния внизу окна
class CustomStatusBar(QStatusBar):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            "QStatusBar { background-color: #ffffff; color: #64748b; border-top: 1px solid #e2e8f0; font-size: 12px; padding: 4px 8px; }"
        )

    def showMessage(self, message, timeout=0):
        super().showMessage(f"  {message}", timeout)


# 13. Базовое диалоговое окно
class CustomDialog(QDialog):

    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setStyleSheet(
            "QDialog { background-color: #ffffff; }"
            "QLabel { font-size: 13px; color: #334155; }"
        )

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.reject()
        else:
            super().keyPressEvent(event)
