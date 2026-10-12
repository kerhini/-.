# Кастомный контейнер для хранения данных (вместо обычного словаря)


class MapEntry:
    # Элемент для хранения пары ключ-значение
    def __init__(self, key, value):
        self._key = key
        self._value = value

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, new_key):
        if new_key is None:
            raise ValueError("Ключ не может быть пустым")
        self._key = new_key

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def __repr__(self) -> str:
        return f"MapEntry({self._key!r}, {self._value!r})"

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
    # Класс ассоциативного массива на основе обычного списка
    def __init__(self):
        self._entries = list()

    @property
    def entries(self) -> list:
        return self._entries

    @entries.setter
    def entries(self, new_entries: list):
        if not isinstance(new_entries, list):
            raise TypeError("Ожидается список list")
        self._entries = new_entries

    # Добавление или обновление значения
    def put(self, key, value):
        for entry in self._entries:
            if entry.key == key:
                entry.value = value
                return
        self._entries.append(MapEntry(key, value))

    # Получение значения по ключу
    def get(self, key, default=None):
        for entry in self._entries:
            if entry.key == key:
                return entry.value
        return default

    # Удаление элемента
    def remove(self, key) -> bool:
        for i in range(len(self._entries)):
            if self._entries[i].key == key:
                self._entries.pop(i)
                return True
        return False

    # Проверка наличия ключа
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

    # Магические методы для удобной работы как со словарем
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
        items_str = ", ".join([f"{e.key!r}: {e.value!r}" for e in self._entries])
        return f"CustomMap([{items_str}])"

    def __str__(self) -> str:
        items_str = ", ".join([f"{e.key}: {e.value}" for e in self._entries])
        return f"CustomMap({items_str})"

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
