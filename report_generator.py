from datetime import datetime


# Класс для сохранения данных о сессии пользователя
class SessionRecord:

    def __init__(self, username, time_in, time_out):
        self._username = ""
        self._time_in = None
        self._time_out = None

        self.username = username
        self.time_in = time_in
        self.time_out = time_out

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, val):
        s = str(val).strip()
        if not s:
            self._username = "admin"
        else:
            self._username = s

    @property
    def time_in(self):
        return self._time_in

    @time_in.setter
    def time_in(self, val):
        if not isinstance(val, datetime):
            raise TypeError("Ожидается объект datetime")
        self._time_in = val

    @property
    def time_out(self):
        return self._time_out

    @time_out.setter
    def time_out(self, val):
        if not isinstance(val, datetime):
            raise TypeError("Ожидается объект datetime")
        self._time_out = val

    def __repr__(self):
        return f"SessionRecord('{self._username}', {self._time_in}, {self._time_out})"

    def __str__(self):
        return f"{self._username} ({self._time_in} - {self._time_out})"

    def __eq__(self, other):
        if not isinstance(other, SessionRecord):
            return False
        return (
            self._username == other._username
            and self._time_in == other._time_in
            and self._time_out == other._time_out
        )


# Генератор отчета в виде таблицы символов
class SessionReportGenerator:

    TIME_FORMAT = "%d.%m.%Y %H:%M:%S"

    @staticmethod
    def format_datetime(dt):
        return dt.strftime(SessionReportGenerator.TIME_FORMAT)

    # Строим таблицу отчета по требованиям
    @staticmethod
    def build_report_table(record):
        user_str = record.username
        t_in_str = SessionReportGenerator.format_datetime(record.time_in)
        t_out_str = SessionReportGenerator.format_datetime(record.time_out)

        # Вычисляем ширину колонок
        col1 = max(len("login"), len(user_str)) + 2
        col2 = max(len("time_in"), len(t_in_str)) + 2
        col3 = max(len("time_out"), len(t_out_str)) + 2

        total_width = col1 + col2 + col3 + 2
        border = "+" + ("-" * total_width) + "+"

        header = f"| {'login'.ljust(col1 - 1)}| {'time_in'.ljust(col2 - 1)}| {'time_out'.ljust(col3 - 1)}|"
        sep = f"|{'-' * col1}|{'-' * col2}|{'-' * col3}|"
        row = f"| {user_str.ljust(col1 - 1)}| {t_in_str.ljust(col2 - 1)}| {t_out_str.ljust(col3 - 1)}|"

        lines = list()
        lines.append(border)
        lines.append(header)
        lines.append(sep)
        lines.append(row)
        lines.append(border)

        return "\n".join(lines)

    # Сохраняем готовую таблицу в файл
    @staticmethod
    def save_report_to_file(record, file_path="session_report.txt"):
        text = SessionReportGenerator.build_report_table(record)
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(text + "\n\n")
        return text
