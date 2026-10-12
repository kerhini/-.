# Своя структура данных вместо словаря (dict)
# Преподаватель запретил использовать встроенный dict, поэтому пишем свой


# Класс одной пары ключ-значение
class MapEntry:

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

    def __repr__(self):
        return f"MapEntry({self._key!r}, {self._value!r})"

    def __str__(self):
        return f"{self._key}: {self._value}"

    def __eq__(self, other):
        if not isinstance(other, MapEntry):
            return False
        return self._key == other._key and self._value == other._value

    def __lt__(self, other):
        if not isinstance(other, MapEntry):
            return NotImplemented
        return str(self._key) < str(other._key)

    def __gt__(self, other):
        if not isinstance(other, MapEntry):
            return NotImplemented
        return str(self._key) > str(other._key)

    def __hash__(self):
        return hash(self._key)


# Класс карты (ассоциативного массива) на основе обычного списка
class CustomMap:

    def __init__(self):
        # Список для хранения объектов MapEntry
        self._entries = list()

    @property
    def entries(self):
        return self._entries

    @entries.setter
    def entries(self, new_entries):
        if not isinstance(new_entries, list):
            raise TypeError("Ожидается список list")
        self._entries = new_entries

    # Добавление или обновление значения по ключу
    def put(self, key, value):
        for item in self._entries:
            if item.key == key:
                item.value = value
                return
        self._entries.append(MapEntry(key, value))

    # Получение значения по ключу
    def get(self, key, default=None):
        for item in self._entries:
            if item.key == key:
                return item.value
        return default

    # Удаление элемента по ключу
    def remove(self, key):
        for i in range(len(self._entries)):
            if self._entries[i].key == key:
                self._entries.pop(i)
                return True
        return False

    # Проверка, есть ли такой ключ
    def contains_key(self, key):
        for item in self._entries:
            if item.key == key:
                return True
        return False

    # Список всех ключей
    def keys(self):
        res = list()
        for item in self._entries:
            res.append(item.key)
        return res

    # Список всех значений
    def values(self):
        res = list()
        for item in self._entries:
            res.append(item.value)
        return res

    # Список пар (ключ, значение)
    def items(self):
        res = list()
        for item in self._entries:
            res.append((item.key, item.value))
        return res

    # Очистить всё
    def clear(self):
        self._entries.clear()

    # Магические методы для работы как со словарем
    def __len__(self):
        return len(self._entries)

    def __getitem__(self, key):
        for item in self._entries:
            if item.key == key:
                return item.value
        raise KeyError(key)

    def __setitem__(self, key, value):
        self.put(key, value)

    def __delitem__(self, key):
        if not self.remove(key):
            raise KeyError(key)

    def __contains__(self, key):
        return self.contains_key(key)

    def __iter__(self):
        for item in self._entries:
            yield item.key

    def __repr__(self):
        parts = list()
        for item in self._entries:
            parts.append(f"{item.key!r}: {item.value!r}")
        return "CustomMap([" + ", ".join(parts) + "])"

    def __str__(self):
        parts = list()
        for item in self._entries:
            parts.append(f"{item.key}: {item.value}")
        return "CustomMap(" + ", ".join(parts) + ")"

    def __eq__(self, other):
        if not isinstance(other, CustomMap):
            return False
        if len(self) != len(other):
            return False
        for item in self._entries:
            if not other.contains_key(item.key):
                return False
            if other.get(item.key) != item.value:
                return False
        return True

    def __bool__(self):
        return len(self._entries) > 0
