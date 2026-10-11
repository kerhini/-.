"""Компоненты пользовательского интерфейса приложения."""

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
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from PyQt6.QtGui import QKeyEvent, QPaintEvent, QMouseEvent


# ─── Глобальная цветовая палитра (Material Design 3 / Slate) ────────────────
_ACCENT       = "#4f46e5"   # indigo-600
_ACCENT_HOVER = "#4338ca"   # indigo-700
_ACCENT_PRESS = "#3730a3"   # indigo-800
_ACCENT_LIGHT = "#e0e7ff"   # indigo-100

_BG_APP    = "#f8fafc"   # slate-50
_BG_CARD   = "#ffffff"
_BG_ROW    = "#f1f5f9"   # slate-100 – чётные строки

_BORDER    = "#e2e8f0"   # slate-200
_BORDER_FO = "#818cf8"   # indigo-400 – focused

_TEXT_H    = "#0f172a"   # slate-900
_TEXT_B    = "#334155"   # slate-700
_TEXT_SUB  = "#64748b"   # slate-500

_RED       = "#ef4444"
_RED_H     = "#dc2626"
_GREEN     = "#22c55e"


# ─── 1. Главное окно ─────────────────────────────────────────────────────────
class CustomMainWindow(QMainWindow):
    """Кастомное главное окно с перехватом закрытия и глобальным фоном."""

    window_closed_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._exit_handler = None
        self.setStyleSheet(f"QMainWindow {{ background-color: {_BG_APP}; }}")

    @property
    def exit_handler(self):
        return self._exit_handler

    @exit_handler.setter
    def exit_handler(self, handler):
        self._exit_handler = handler

    def closeEvent(self, event):
        """Переопределение: вызов обработчика сохранения отчёта перед выходом."""
        if self._exit_handler is not None:
            self._exit_handler()
        self.window_closed_signal.emit()
        event.accept()

    def keyPressEvent(self, event: QKeyEvent):
        """Переопределение: Escape не закрывает окно."""
        if event.key() == Qt.Key.Key_Escape:
            event.ignore()
        else:
            super().keyPressEvent(event)


# ─── 2. Кнопка ───────────────────────────────────────────────────────────────
class CustomButton(QPushButton):
    """Кастомная кнопка: primary / secondary / danger с hover-эффектами."""

    def __init__(self, text: str = "", primary: bool = False,
                 danger: bool = False, parent=None):
        super().__init__(text, parent)
        self._primary = primary
        self._danger = danger
        self._refresh_style()

    @property
    def is_primary(self) -> bool:
        return self._primary

    @is_primary.setter
    def is_primary(self, val: bool):
        self._primary = bool(val)
        self._refresh_style()

    @staticmethod
    def _style_primary() -> str:
        """Строка QSS для primary-кнопки (@staticmethod)."""
        return (
            f"QPushButton {{"
            f"  background-color: {_ACCENT};"
            f"  color: #ffffff;"
            f"  font-weight: 600;"
            f"  font-size: 13px;"
            f"  border-radius: 8px;"
            f"  padding: 8px 20px;"
            f"  border: none;"
            f"}}"
            f"QPushButton:hover  {{ background-color: {_ACCENT_HOVER}; }}"
            f"QPushButton:pressed {{ background-color: {_ACCENT_PRESS}; }}"
            f"QPushButton:disabled {{ background-color: #94a3b8; }}"
        )

    @staticmethod
    def _style_secondary() -> str:
        """Строка QSS для secondary-кнопки (@staticmethod)."""
        return (
            f"QPushButton {{"
            f"  background-color: {_BG_CARD};"
            f"  color: {_TEXT_B};"
            f"  font-weight: 500;"
            f"  font-size: 13px;"
            f"  border-radius: 8px;"
            f"  padding: 8px 18px;"
            f"  border: 1px solid {_BORDER};"
            f"}}"
            f"QPushButton:hover  {{ background-color: {_BG_ROW}; border-color: #94a3b8; }}"
            f"QPushButton:pressed {{ background-color: {_BORDER}; }}"
            f"QPushButton:disabled {{ color: #94a3b8; }}"
        )

    @staticmethod
    def _style_danger() -> str:
        """Строка QSS для danger-кнопки (@staticmethod)."""
        return (
            f"QPushButton {{"
            f"  background-color: {_BG_CARD};"
            f"  color: {_RED};"
            f"  font-weight: 500;"
            f"  font-size: 13px;"
            f"  border-radius: 8px;"
            f"  padding: 8px 18px;"
            f"  border: 1px solid #fecaca;"
            f"}}"
            f"QPushButton:hover  {{ background-color: #fff1f2; border-color: {_RED}; }}"
            f"QPushButton:pressed {{ background-color: #fee2e2; }}"
        )

    def _refresh_style(self):
        if self._danger:
            self.setStyleSheet(CustomButton._style_danger())
        elif self._primary:
            self.setStyleSheet(CustomButton._style_primary())
        else:
            self.setStyleSheet(CustomButton._style_secondary())

    def enterEvent(self, event):
        """Переопределение: рука при наведении."""
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Переопределение: сброс курсора."""
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        """Переопределение нажатия мыши."""
        super().mousePressEvent(event)


# ─── 3. Поле ввода ───────────────────────────────────────────────────────────
class CustomLineEdit(QLineEdit):
    """Кастомное текстовое поле с подсветкой фокуса."""

    enter_pressed_signal = pyqtSignal()

    def __init__(self, placeholder: str = "", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setMinimumHeight(36)
        self._set_style(False)

    def _set_style(self, focused: bool):
        border = _BORDER_FO if focused else _BORDER
        width  = "2px"       if focused else "1px"
        self.setStyleSheet(
            f"QLineEdit {{"
            f"  border: {width} solid {border};"
            f"  border-radius: 8px;"
            f"  padding: 4px 12px;"
            f"  background-color: {_BG_CARD};"
            f"  color: {_TEXT_H};"
            f"  font-size: 13px;"
            f"}}"
        )

    def focusInEvent(self, event):
        """Переопределение: акцент при фокусе."""
        self._set_style(True)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        """Переопределение: обычный стиль без фокуса."""
        self._set_style(False)
        super().focusOutEvent(event)

    def keyPressEvent(self, event: QKeyEvent):
        """Переопределение: Enter как сигнал."""
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.enter_pressed_signal.emit()
        super().keyPressEvent(event)


# ─── 4. Метка ────────────────────────────────────────────────────────────────
class CustomLabel(QLabel):
    """Кастомная метка: обычная / заголовок / подзаголовок."""

    def __init__(self, text: str = "", is_title: bool = False,
                 is_sub: bool = False, parent=None):
        super().__init__(text, parent)
        if is_title:
            self.setStyleSheet(
                f"font-size: 15px; font-weight: 700; color: {_TEXT_H};"
            )
        elif is_sub:
            self.setStyleSheet(
                f"font-size: 12px; color: {_TEXT_SUB};"
            )
        else:
            self.setStyleSheet(
                f"font-size: 13px; color: {_TEXT_B};"
            )

    def paintEvent(self, event: QPaintEvent):
        """Переопределение отрисовки метки."""
        super().paintEvent(event)


# ─── 5. Таблица ──────────────────────────────────────────────────────────────
class CustomTableWidget(QTableWidget):
    """Кастомная таблица: зебра-строки, Delete-сигнал, сетка в стиле приложения."""

    delete_requested_signal = pyqtSignal()

    def __init__(self, rows: int = 0, columns: int = 0, parent=None):
        super().__init__(rows, columns, parent)
        self.setAlternatingRowColors(True)
        self.verticalHeader().setVisible(False)
        self.setShowGrid(True)
        self.setWordWrap(False)
        self.verticalHeader().setDefaultSectionSize(40)
        self.setStyleSheet(
            f"QTableWidget {{"
            f"  background-color: {_BG_CARD};"
            f"  alternate-background-color: {_BG_ROW};"
            f"  gridline-color: {_BORDER};"
            f"  border: 1px solid {_BORDER};"
            f"  border-radius: 10px;"
            f"  font-size: 13px;"
            f"  color: {_TEXT_B};"
            f"  selection-background-color: {_ACCENT_LIGHT};"
            f"  selection-color: {_TEXT_H};"
            f"  outline: none;"
            f"}}"
            f"QHeaderView::section {{"
            f"  background-color: {_BG_ROW};"
            f"  color: {_TEXT_SUB};"
            f"  font-size: 12px;"
            f"  font-weight: 600;"
            f"  text-transform: uppercase;"
            f"  letter-spacing: 0.5px;"
            f"  padding: 8px 10px;"
            f"  border: none;"
            f"  border-bottom: 2px solid {_BORDER};"
            f"  border-right: 1px solid {_BORDER};"
            f"}}"
            f"QScrollBar:vertical {{"
            f"  background: {_BG_ROW}; width: 8px; border-radius: 4px;"
            f"}}"
            f"QScrollBar::handle:vertical {{"
            f"  background: #cbd5e1; border-radius: 4px; min-height: 30px;"
            f"}}"
            f"QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}"
        )

    def keyPressEvent(self, event: QKeyEvent):
        """Переопределение: Delete = сигнал на удаление."""
        if event.key() == Qt.Key.Key_Delete:
            self.delete_requested_signal.emit()
        else:
            super().keyPressEvent(event)


# ─── 6. Комбобокс ────────────────────────────────────────────────────────────
class CustomComboBox(QComboBox):
    """Кастомный выпадающий список без скролла по колесу мыши в закрытом виде."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(36)
        self.setStyleSheet(
            f"QComboBox {{"
            f"  border: 1px solid {_BORDER};"
            f"  border-radius: 8px;"
            f"  padding: 4px 12px;"
            f"  background-color: {_BG_CARD};"
            f"  color: {_TEXT_H};"
            f"  font-size: 13px;"
            f"}}"
            f"QComboBox:hover {{ border-color: #94a3b8; }}"
            f"QComboBox::drop-down {{"
            f"  border: none; width: 28px;"
            f"}}"
            f"QComboBox::down-arrow {{"
            f"  image: none;"
            f"  border-left: 4px solid transparent;"
            f"  border-right: 4px solid transparent;"
            f"  border-top: 6px solid {_TEXT_SUB};"
            f"  margin-right: 8px;"
            f"}}"
            f"QComboBox QAbstractItemView {{"
            f"  border: 1px solid {_BORDER};"
            f"  border-radius: 8px;"
            f"  background: {_BG_CARD};"
            f"  selection-background-color: {_ACCENT_LIGHT};"
            f"  selection-color: {_TEXT_H};"
            f"  padding: 4px;"
            f"  font-size: 13px;"
            f"}}"
        )

    def wheelEvent(self, event):
        """Переопределение: запрет скролла когда закрыт."""
        if not self.view().isVisible():
            event.ignore()
        else:
            super().wheelEvent(event)

    def showPopup(self):
        """Переопределение показа всплывающего списка."""
        super().showPopup()


# ─── 7. Числовое поле (SpinBox) ──────────────────────────────────────────────
class CustomSpinBox(QDoubleSpinBox):
    """Кастомный спинбокс без нечаянного скролла."""

    def __init__(self, minimum: float = 0.0, maximum: float = 999999.0,
                 step: float = 1.0, parent=None):
        super().__init__(parent)
        self.setRange(minimum, maximum)
        self.setSingleStep(step)
        self.setMinimumHeight(36)
        self.setStyleSheet(
            f"QDoubleSpinBox {{"
            f"  border: 1px solid {_BORDER};"
            f"  border-radius: 8px;"
            f"  padding: 4px 10px;"
            f"  background-color: {_BG_CARD};"
            f"  color: {_TEXT_H};"
            f"  font-size: 13px;"
            f"}}"
            f"QDoubleSpinBox:focus {{ border: 2px solid {_BORDER_FO}; }}"
            f"QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{"
            f"  border: none; background: transparent; width: 18px;"
            f"}}"
        )

    def wheelEvent(self, event):
        """Переопределение: скролл только при фокусе."""
        if not self.hasFocus():
            event.ignore()
        else:
            super().wheelEvent(event)

    def stepBy(self, steps: int):
        """Переопределение шага изменения значения."""
        super().stepBy(steps)


# ─── 8. Флажок ───────────────────────────────────────────────────────────────
class CustomCheckBox(QCheckBox):
    """Кастомный чекбокс с расширенной зоной клика."""

    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(
            f"QCheckBox {{"
            f"  color: {_TEXT_B};"
            f"  font-size: 13px;"
            f"  spacing: 8px;"
            f"}}"
            f"QCheckBox::indicator {{"
            f"  width: 18px; height: 18px;"
            f"  border-radius: 5px;"
            f"  border: 2px solid {_BORDER};"
            f"  background: {_BG_CARD};"
            f"}}"
            f"QCheckBox::indicator:checked {{"
            f"  background: {_ACCENT};"
            f"  border-color: {_ACCENT};"
            f"}}"
            f"QCheckBox::indicator:hover {{"
            f"  border-color: {_ACCENT};"
            f"}}"
        )

    def nextCheckState(self):
        """Переопределение смены состояния флажка."""
        super().nextCheckState()

    def hitButton(self, pos: QPoint) -> bool:
        """Переопределение области нажатия."""
        return super().hitButton(pos)


# ─── 9. Прогресс-бар ─────────────────────────────────────────────────────────
class CustomProgressBar(QProgressBar):
    """Кастомная полоса прогресса с переопределённой отрисовкой."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTextVisible(True)
        self.setRange(0, 100)
        self.setValue(0)
        self.setFixedHeight(22)
        self.setStyleSheet(
            f"QProgressBar {{"
            f"  border: none;"
            f"  border-radius: 11px;"
            f"  text-align: center;"
            f"  color: {_TEXT_H};"
            f"  font-size: 12px;"
            f"  font-weight: 600;"
            f"  background-color: {_BG_ROW};"
            f"}}"
            f"QProgressBar::chunk {{"
            f"  background: qlineargradient("
            f"    x1:0, y1:0, x2:1, y2:0,"
            f"    stop:0 {_ACCENT}, stop:1 #818cf8"
            f"  );"
            f"  border-radius: 11px;"
            f"}}"
        )

    def paintEvent(self, event: QPaintEvent):
        """Переопределение отрисовки."""
        super().paintEvent(event)


# ─── 10. Многострочный редактор ──────────────────────────────────────────────
class CustomTextEdit(QTextEdit):
    """Кастомный текстовый редактор с переопределением фокуса."""

    def __init__(self, placeholder: str = "", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setStyleSheet(
            f"QTextEdit {{"
            f"  border: 1px solid {_BORDER};"
            f"  border-radius: 8px;"
            f"  padding: 8px 10px;"
            f"  background-color: {_BG_CARD};"
            f"  color: {_TEXT_B};"
            f"  font-size: 13px;"
            f"  line-height: 1.5;"
            f"}}"
            f"QTextEdit:focus {{ border: 2px solid {_BORDER_FO}; }}"
        )

    def focusInEvent(self, event):
        """Переопределение получения фокуса."""
        super().focusInEvent(event)

    def keyPressEvent(self, event: QKeyEvent):
        """Переопределение ввода с клавиатуры."""
        super().keyPressEvent(event)


# ─── 11. Групповой контейнер ─────────────────────────────────────────────────
class CustomGroupBox(QGroupBox):
    """Кастомный GroupBox с аккуратной карточкой."""

    def __init__(self, title: str = "", parent=None):
        super().__init__(title, parent)
        self.setStyleSheet(
            f"QGroupBox {{"
            f"  font-size: 12px;"
            f"  font-weight: 600;"
            f"  color: {_TEXT_SUB};"
            f"  text-transform: uppercase;"
            f"  letter-spacing: 0.5px;"
            f"  border: 1px solid {_BORDER};"
            f"  border-radius: 12px;"
            f"  margin-top: 16px;"
            f"  padding-top: 8px;"
            f"  background-color: {_BG_CARD};"
            f"}}"
            f"QGroupBox::title {{"
            f"  subcontrol-origin: margin;"
            f"  left: 14px;"
            f"  padding: 0 8px;"
            f"  background: {_BG_CARD};"
            f"}}"
        )

    def paintEvent(self, event: QPaintEvent):
        """Переопределение отрисовки группы."""
        super().paintEvent(event)


# ─── 12. Строка состояния ────────────────────────────────────────────────────
class CustomStatusBar(QStatusBar):
    """Кастомная строка состояния с форматированием сообщений."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            f"QStatusBar {{"
            f"  background-color: {_BG_CARD};"
            f"  border-top: 1px solid {_BORDER};"
            f"  color: {_TEXT_SUB};"
            f"  font-size: 12px;"
            f"  padding: 4px 14px;"
            f"}}"
        )

    def showMessage(self, message: str, timeout: int = 0):
        """Переопределение: добавляет точку-маркер статуса."""
        super().showMessage(f"  {message}", timeout)


# ─── 13. Диалоговое окно ─────────────────────────────────────────────────────
class CustomDialog(QDialog):
    """Кастомное диалоговое окно с перехватом Escape и стилизацией."""

    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setStyleSheet(
            f"QDialog {{ background-color: {_BG_CARD}; }}"
            f"QLabel {{ color: {_TEXT_B}; }}"
        )

    def keyPressEvent(self, event: QKeyEvent):
        """Переопределение: Escape закрывает диалог через reject()."""
        if event.key() == Qt.Key.Key_Escape:
            self.reject()
        else:
            super().keyPressEvent(event)

    def closeEvent(self, event):
        """Переопределение закрытия диалогового окна."""
        super().closeEvent(event)
