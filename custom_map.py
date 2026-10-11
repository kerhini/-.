"""
Модуль пользовательской структуры данных для маппинга (CustomMap).
В соответствии с требованиями ТЗ:
- Запрещено использовать Map (dict). Для маппинга используется собственный кастомный класс.
- Все сущности описаны через классы.
- Вся функциональность реализована через методы класса или объекта.
- Кастомный класс реализует специальные методы, гетеры/сеттеры и сравнение.
"""


class MapEntry:
    """Элемент пары 'ключ-значение' для пользовательской карты CustomMap."""

    def __init__(self, key, value):
        self._key = key
        self._value = value

    @property
    def key(self):
        """Геттер ключа."""
        return self._key

    @key.setter
    def key(self, new_key):
        """Сеттер ключа с валидацией."""
        if new_key is None:
            raise ValueError("Ключ не может быть None")
        self._key = new_key

    @property
    def value(self):
        """Геттер значения."""
        return self._value

    @value.setter
    def value(self, new_value):
        """Сеттер значения."""
        self._value = new_value

    def __repr__(self) -> str:
        return f"MapEntry(key={self._key!r}, value={self._value!r})"

    def __str__(self) -> str:
        return f"{self._key}: {self._value}"

    def __eq__(self, other) -> bool:
        if not isinstance(other, MapEntry):
            return False
        return self._key == other._key and self._value == other._value

    def __lt__(self, other) -> bool:
        if not isinstance(other, MapEntry):
            return NotImplemented
        return str(self._key) < str(other._key)

    def __gt__(self, other) -> bool:
        if not isinstance(other, MapEntry):
            return NotImplemented
        return str(self._key) > str(other._key)

    def __hash__(self) -> int:
        return hash(self._key)


class CustomMap:
    """
    Кастомная реализация структуры 'Ключ-Значение' без использования встроенного dict.
    Внутри используется упорядоченный список объектов MapEntry.
    """

    def __init__(self):
        # Хранилище записей на основе списка пользовательских объектов MapEntry
        self._entries = list()

    @property
    def entries(self) -> list:
        """Геттер внутреннего списка записей."""
        return self._entries

    @entries.setter
    def entries(self, new_entries: list):
        """Сеттер списка записей с валидацией."""
        if not isinstance(new_entries, list):
            raise TypeError("Список записей должен быть экземпляром list")
        self._entries = new_entries

    def put(self, key, value):
        """Добавить или обновить пару ключ-значение."""
        for entry in self._entries:
            if entry.key == key:
                entry.value = value
                return
        self._entries.append(MapEntry(key, value))

    def get(self, key, default=None):
        """Получить значение по ключу, либо default."""
        for entry in self._entries:
            if entry.key == key:
                return entry.value
        return default

    def remove(self, key) -> bool:
        """Удалить запись по ключу. Возвращает True, если найдено и удалено."""
        for index in range(len(self._entries)):
            if self._entries[index].key == key:
                self._entries.pop(index)
                return True
        return False

    def contains_key(self, key) -> bool:
        """Проверка наличия ключа."""
        for entry in self._entries:
            if entry.key == key:
                return True
        return False

    def keys(self) -> list:
        """Получить список всех ключей."""
        result = list()
        for entry in self._entries:
            result.append(entry.key)
        return result

    def values(self) -> list:
        """Получить список всех значений."""
        result = list()
        for entry in self._entries:
            result.append(entry.value)
        return result

    def items(self) -> list:
        """Получить список пар (ключ, значение) в виде кортежей."""
        result = list()
        for entry in self._entries:
            result.append((entry.key, entry.value))
        return result

    def clear(self):
        """Очистить карту."""
        self._entries.clear()

    # --- Специальные методы (dunder methods) ---

    def __len__(self) -> int:
        return len(self._entries)

    def __getitem__(self, key):
        for entry in self._entries:
            if entry.key == key:
                return entry.value
        raise KeyError(f"Ключ {key!r} не найден в CustomMap")

    def __setitem__(self, key, value):
        self.put(key, value)

    def __delitem__(self, key):
        if not self.remove(key):
            raise KeyError(f"Ключ {key!r} не найден для удаления в CustomMap")

    def __contains__(self, key) -> bool:
        return self.contains_key(key)

    def __iter__(self):
        for entry in self._entries:
            yield entry.key

    def __repr__(self) -> str:
        parts = list()
        for entry in self._entries:
            parts.append(f"{entry.key!r}: {entry.value!r}")
        joined = ", ".join(parts)
        return f"CustomMap([{joined}])"

    def __str__(self) -> str:
        parts = list()
        for entry in self._entries:
            parts.append(f"{entry.key}: {entry.value}")
        joined = ", ".join(parts)
        return f"CustomMap({joined})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, CustomMap):
            return False
        if len(self) != len(other):
            return False
        for entry in self._entries:
            if not other.contains_key(entry.key) or other.get(entry.key) != entry.value:
                return False
        return True

    def __bool__(self) -> bool:
        return len(self._entries) > 0
