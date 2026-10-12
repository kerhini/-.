from datetime import datetime


# Класс для хранения данных о сессии пользователя
class SessionRecord:

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
        val_str = str(val).strip()
        if not val_str:
            self._username = "admin"
        else:
            self._username = val_str

    @property
    def time_in(self) -> datetime:
        return self._time_in

    @time_in.setter
    def time_in(self, val: datetime):
        if not isinstance(val, datetime):
            raise TypeError("Ожидается объект datetime для time_in")
        self._time_in = val

    @property
    def time_out(self) -> datetime:
        return self._time_out

    @time_out.setter
    def time_out(self, val: datetime):
        if not isinstance(val, datetime):
            raise TypeError("Ожидается объект datetime для time_out")
        self._time_out = val

    def __repr__(self) -> str:
        return f"SessionRecord('{self._username}', {self._time_in}, {self._time_out})"

    def __str__(self) -> str:
        return f"{self._username} ({self._time_in} - {self._time_out})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, SessionRecord):
            return False
        return (
            self._username == other._username
            and self._time_in == other._time_in
            and self._time_out == other._time_out
        )


# Класс для формирования отчета о сессии в текстовую таблицу
class SessionReportGenerator:

    TIME_FORMAT = "%d.%m.%Y %H:%M:%S"

    @staticmethod
    def format_datetime(dt: datetime) -> str:
        return dt.strftime(SessionReportGenerator.TIME_FORMAT)

    @staticmethod
    def build_report_table(record: SessionRecord) -> str:
        login_str = record.username
        time_in_str = SessionReportGenerator.format_datetime(record.time_in)
        time_out_str = SessionReportGenerator.format_datetime(record.time_out)

        # Вычисляем ширину колонок таблицы
        w1 = max(len("login"), len(login_str)) + 2
        w2 = max(len("time_in"), len(time_in_str)) + 2
        w3 = max(len("time_out"), len(time_out_str)) + 2

        full_width = w1 + w2 + w3 + 2
        border = "+" + ("-" * full_width) + "+"

        header = f"| {'login'.ljust(w1 - 1)}| {'time_in'.ljust(w2 - 1)}| {'time_out'.ljust(w3 - 1)}|"
        divider = f"|{'-' * w1}|{'-' * w2}|{'-' * w3}|"
        data = f"| {login_str.ljust(w1 - 1)}| {time_in_str.ljust(w2 - 1)}| {time_out_str.ljust(w3 - 1)}|"

        lines = list()
        lines.append(border)
        lines.append(header)
        lines.append(divider)
        lines.append(data)
        lines.append(border)

        return "\n".join(lines)

    @staticmethod
    def save_report_to_file(record: SessionRecord, file_path: str = "session_report.txt") -> str:
        table_str = SessionReportGenerator.build_report_table(record)
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(table_str + "\n\n")
        return table_str
