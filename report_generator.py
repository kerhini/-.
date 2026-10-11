"""
Модуль формирования отчета о сессии пользователя.
В соответствии с требованиями ТЗ:
- При закрытии приложения должен быть сохранен в файл отчет о работе приложения в формате:
  +------------------------------------+
  | login | time_in | time_out |
  |---------|------------|-------------|
  |UserName | <datetime> | <datetime> |
  +------------------------------------+
  формат времени %d.%m.%Y %H:%M:%S
- Все функции реализованы внутри классов (@staticmethod или методы объекта).
- Запрещено использовать dict.
"""

from datetime import datetime


class SessionRecord:
    """Класс записи пользовательской сессии."""

    def __init__(self, username: str, time_in: datetime, time_out: datetime):
        self._username = ""
        self._time_in = None
        self._time_out = None

        self.username = username
        self.time_in = time_in
        self.time_out = time_out

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, val: str):
        if not isinstance(val, str) or not val.strip():
            self._username = "Admin"
        else:
            self._username = val.strip()

    @property
    def time_in(self) -> datetime:
        return self._time_in

    @time_in.setter
    def time_in(self, val: datetime):
        if not isinstance(val, datetime):
            raise TypeError("time_in должен быть объектом datetime")
        self._time_in = val

    @property
    def time_out(self) -> datetime:
        return self._time_out

    @time_out.setter
    def time_out(self, val: datetime):
        if not isinstance(val, datetime):
            raise TypeError("time_out должен быть объектом datetime")
        self._time_out = val

    def __repr__(self) -> str:
        return f"SessionRecord(username={self._username!r}, time_in={self._time_in}, time_out={self._time_out})"

    def __str__(self) -> str:
        return f"{self._username} ({self._time_in} -> {self._time_out})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, SessionRecord):
            return False
        return (
            self._username == other._username
            and self._time_in == other._time_in
            and self._time_out == other._time_out
        )


class SessionReportGenerator:
    """
    Класс для генерации и сохранения отчета о работе приложения.
    Форматирует таблицу точно в соответствии с заданием преподавателя.
    """

    TIME_FORMAT = "%d.%m.%Y %H:%M:%S"

    @staticmethod
    def format_datetime(dt: datetime) -> str:
        """Форматирование даты и времени по обязательному шаблону (%d.%m.%Y %H:%M:%S)."""
        return dt.strftime(SessionReportGenerator.TIME_FORMAT)

    @staticmethod
    def build_report_table(record: SessionRecord) -> str:
        """
        Построить ASCII-таблицу сессии точно по формату:
        +------------------------------------+
        | login    | time_in             | time_out            |
        |----------|---------------------|---------------------|
        | UserName | <datetime>          | <datetime>          |
        +------------------------------------+
        """
        login_str = record.username
        time_in_str = SessionReportGenerator.format_datetime(record.time_in)
        time_out_str = SessionReportGenerator.format_datetime(record.time_out)

        # Вычисление ширины колонок для аккуратного выравнивания
        col1_len = max(len("login"), len(login_str)) + 2
        col2_len = max(len("time_in"), len(time_in_str)) + 2
        col3_len = max(len("time_out"), len(time_out_str)) + 2

        inner_width = col1_len + col2_len + col3_len + 2  # для 2 внутренних разделителей '|'
        border_line = "+" + ("-" * inner_width) + "+"

        header_line = (
            f"| {'login'.ljust(col1_len - 1)}"
            f"| {'time_in'.ljust(col2_len - 1)}"
            f"| {'time_out'.ljust(col3_len - 1)}|"
        )

        divider_line = (
            f"|{'-' * col1_len}"
            f"|{'-' * col2_len}"
            f"|{'-' * col3_len}|"
        )

        data_line = (
            f"| {login_str.ljust(col1_len - 1)}"
            f"| {time_in_str.ljust(col2_len - 1)}"
            f"| {time_out_str.ljust(col3_len - 1)}|"
        )

        lines = list()
        lines.append(border_line)
        lines.append(header_line)
        lines.append(divider_line)
        lines.append(data_line)
        lines.append(border_line)

        return "\n".join(lines)

    @staticmethod
    def save_report_to_file(record: SessionRecord, file_path: str = "session_report.txt") -> str:
        """Сохранить отчет в текстовый файл (@staticmethod)."""
        table_text = SessionReportGenerator.build_report_table(record)
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(table_text + "\n\n")
        return table_text
