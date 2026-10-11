"""Кастомная структура данных: маппинг ключ-значение без использования dict."""


class MapEntry:
    """Пара ключ-значение."""

    def __init__(self, key, value):
        self._key = key
        self._value = value

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, new_key):
        if new_key is None:
            raise ValueError("Ключ не может быть None")
        self._key = new_key

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
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
    """Ассоциативный контейнер на основе списка пар MapEntry."""

    def __init__(self):
        self._entries = list()

    @property
    def entries(self) -> list:
        return self._entries

    @entries.setter
    def entries(self, new_entries: list):
        if not isinstance(new_entries, list):
            raise TypeError("Ожидается list")
        self._entries = new_entries

    def put(self, key, value):
        """Добавить или обновить запись."""
        for entry in self._entries:
            if entry.key == key:
                entry.value = value
                return
        self._entries.append(MapEntry(key, value))

    def get(self, key, default=None):
        """Получить значение по ключу."""
        for entry in self._entries:
            if entry.key == key:
                return entry.value
        return default

    def remove(self, key) -> bool:
        """Удалить запись по ключу."""
        for index in range(len(self._entries)):
            if self._entries[index].key == key:
                self._entries.pop(index)
                return True
        return False

    def contains_key(self, key) -> bool:
        for entry in self._entries:
            if entry.key == key:
                return True
        return False

    def keys(self) -> list:
        return [entry.key for entry in self._entries]

    def values(self) -> list:
        return [entry.value for entry in self._entries]

    def items(self) -> list:
        return [(entry.key, entry.value) for entry in self._entries]

    def clear(self):
        self._entries.clear()

    def __len__(self) -> int:
        return len(self._entries)

    def __getitem__(self, key):
        for entry in self._entries:
            if entry.key == key:
                return entry.value
        raise KeyError(key)

    def __setitem__(self, key, value):
        self.put(key, value)

    def __delitem__(self, key):
        if not self.remove(key):
            raise KeyError(key)

    def __contains__(self, key) -> bool:
        return self.contains_key(key)

    def __iter__(self):
        for entry in self._entries:
            yield entry.key

    def __repr__(self) -> str:
        parts = [f"{e.key!r}: {e.value!r}" for e in self._entries]
        return f"CustomMap([{', '.join(parts)}])"

    def __str__(self) -> str:
        parts = [f"{e.key}: {e.value}" for e in self._entries]
        return f"CustomMap({', '.join(parts)})"

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
