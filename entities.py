"""
Модуль сущностей предметной области (Складской учёт / Каталог товаров).
В соответствии с требованиями ТЗ:
- Все сущности описаны через классы.
- Сущности наследованы от абстрактного класса (BaseEntity).
- Пользовательские классы переопределяют более 3 спец. методов + __eq__, __repr__, __str__.
- Пользовательские классы сравнимы (реализованы __lt__, __gt__, __le__, __ge__).
- Все атрибуты имеют геттеры и сеттеры (@property и @setter).
- Вся функциональность реализована через методы класса (@staticmethod) или объекта.
- Не используется встроенный словарь dict.
"""

from abc import ABC, abstractmethod


class BaseEntity(ABC):
    """
    Абстрактный базовый класс для всех сущностей приложения.
    Определяет обязательный интерфейс жизненного цикла сущностей.
    """

    @abstractmethod
    def get_id(self) -> int:
        """Получить уникальный идентификатор сущности."""
        pass

    @abstractmethod
    def get_display_name(self) -> str:
        """Получить строковое имя для отображения в интерфейсе."""
        pass

    @abstractmethod
    def validate(self) -> bool:
        """Проверить корректность данных сущности."""
        pass

    @abstractmethod
    def to_row(self) -> list:
        """Преобразовать сущность в строку таблицы интерфейса."""
        pass


class Product(BaseEntity):
    """
    Пользовательский класс товара на складе.
    Наследуется от BaseEntity, содержит инкапсулированные атрибуты с геттерами и сеттерами,
    полноценное сравнение и набор специальных методов.
    """

    def __init__(
        self,
        product_id: int,
        name: str,
        category: str,
        price: float,
        quantity: int,
        barcode: str,
        rating: float,
        description: str,
    ):
        self._id = 0
        self._name = ""
        self._category = ""
        self._price = 0.0
        self._quantity = 0
        self._barcode = ""
        self._rating = 0.0
        self._description = ""

        # Установка через сеттеры для прохождения валидации
        self.id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity
        self.barcode = barcode
        self.rating = rating
        self.description = description

    # --- Геттеры и Сеттеры для всех атрибутов ---

    @property
    def id(self) -> int:
        """Геттер идентификатора товара."""
        return self._id

    @id.setter
    def id(self, value: int):
        """Сеттер идентификатора товара."""
        if not isinstance(value, int) or value < 0:
            raise ValueError("ID товара должен быть неотрицательным целым числом")
        self._id = value

    @property
    def name(self) -> str:
        """Геттер наименования товара."""
        return self._name

    @name.setter
    def name(self, value: str):
        """Сеттер наименования товара."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Наименование товара не может быть пустой строкой")
        self._name = value.strip()

    @property
    def category(self) -> str:
        """Геттер категории товара."""
        return self._category

    @category.setter
    def category(self, value: str):
        """Сеттер категории товара."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Категория товара не может быть пустой строкой")
        self._category = value.strip()

    @property
    def price(self) -> float:
        """Геттер цены товара."""
        return self._price

    @price.setter
    def price(self, value: float):
        """Сеттер цены товара."""
        num_val = float(value)
        if num_val < 0.0:
            raise ValueError("Цена товара не может быть отрицательной")
        self._price = round(num_val, 2)

    @property
    def quantity(self) -> int:
        """Геттер количества на складе."""
        return self._quantity

    @quantity.setter
    def quantity(self, value: int):
        """Сеттер количества на складе."""
        int_val = int(value)
        if int_val < 0:
            raise ValueError("Количество товара не может быть отрицательным")
        self._quantity = int_val

    @property
    def barcode(self) -> str:
        """Геттер штрихкода."""
        return self._barcode

    @barcode.setter
    def barcode(self, value: str):
        """Сеттер штрихкода."""
        if not isinstance(value, str):
            raise TypeError("Штрихкод должен быть строкой")
        self._barcode = value.strip()

    @property
    def rating(self) -> float:
        """Геттер пользовательского рейтинга товара (0.0 - 5.0)."""
        return self._rating

    @rating.setter
    def rating(self, value: float):
        """Сеттер рейтинга товара."""
        num_val = float(value)
        if num_val < 0.0 or num_val > 5.0:
            raise ValueError("Рейтинг должен быть в диапазоне от 0.0 до 5.0")
        self._rating = round(num_val, 1)

    @property
    def description(self) -> str:
        """Геттер описания товара."""
        return self._description

    @description.setter
    def description(self, value: str):
        """Сеттер описания товара."""
        if not isinstance(value, str):
            raise TypeError("Описание должно быть строкой")
        self._description = value.strip()

    # --- Реализация методов абстрактного базового класса BaseEntity ---

    def get_id(self) -> int:
        return self._id

    def get_display_name(self) -> str:
        return self._name

    def validate(self) -> bool:
        """Проверка валидности состояния объекта."""
        return (
            self._id >= 0
            and len(self._name) > 0
            and len(self._category) > 0
            and self._price >= 0.0
            and self._quantity >= 0
            and (0.0 <= self._rating <= 5.0)
        )

    def to_row(self) -> list:
        """Преобразование данных товара в список ячеек для QTableWidget."""
        row_items = list()
        row_items.append(str(self._id))
        row_items.append(self._name)
        row_items.append(self._category)
        row_items.append(f"{self._price:,.2f} \u0440\u0443\u0431.")
        row_items.append(str(self._quantity))
        row_items.append(self._barcode)
        row_items.append(f"{self._rating:.1f} \u2605")
        return row_items


    # --- Обязательные специальные методы: __eq__, __repr__, __str__ ---

    def __repr__(self) -> str:
        return (
            f"Product(id={self._id}, name={self._name!r}, category={self._category!r}, "
            f"price={self._price}, quantity={self._quantity}, barcode={self._barcode!r}, "
            f"rating={self._rating})"
        )

    def __str__(self) -> str:
        return f"Товар №{self._id}: '{self._name}' ({self._category}) - {self._price:.2f} руб. [{self._quantity} шт.]"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Product):
            return False
        return self._id == other._id and self._barcode == other._barcode

    # --- Дополнительные специальные методы (требуется как минимум 3 сверх __eq__, __repr__, __str__) ---

    def __lt__(self, other) -> bool:
        """Сравнение 'меньше' для сортировки (по цене, затем по ID)."""
        if not isinstance(other, Product):
            return NotImplemented
        if self._price != other._price:
            return self._price < other._price
        return self._id < other._id

    def __gt__(self, other) -> bool:
        """Сравнение 'больше'."""
        if not isinstance(other, Product):
            return NotImplemented
        if self._price != other._price:
            return self._price > other._price
        return self._id > other._id

    def __le__(self, other) -> bool:
        """Сравнение 'меньше или равно'."""
        if not isinstance(other, Product):
            return NotImplemented
        return self < other or self == other

    def __ge__(self, other) -> bool:
        """Сравнение 'больше или равно'."""
        if not isinstance(other, Product):
            return NotImplemented
        return self > other or self == other

    def __ne__(self, other) -> bool:
        """Сравнение 'не равно'."""
        return not self.__eq__(other)

    def __hash__(self) -> int:
        """Хеширование для возможности добавления в set и использования в качестве ключа."""
        return hash((self._id, self._barcode))

    def __bool__(self) -> bool:
        """Проверка наличия на складе (True если quantity > 0)."""
        return self._quantity > 0

    def __float__(self) -> float:
        """Приведение к float возвращает стоимость товара."""
        return float(self._price)

    def __int__(self) -> int:
        """Приведение к int возвращает остаток на складе."""
        return int(self._quantity)

    def __len__(self) -> int:
        """Возвращает длину описания товара."""
        return len(self._description)


class ProductRepository:
    """
    Класс-репозиторий для управления коллекцией товаров.
    Вся логика реализована через методы объекта и статические методы (@staticmethod).
    """

    def __init__(self):
        # Хранение не менее 10 пользовательских объектов в коллекции list
        self._items = list()

    @property
    def items(self) -> list:
        return self._items

    @items.setter
    def items(self, new_items: list):
        if not isinstance(new_items, list):
            raise TypeError("Товары должны храниться в списке list")
        self._items = new_items

    def add(self, product: Product):
        """Добавить товар в коллекцию."""
        if not isinstance(product, Product):
            raise TypeError("Объект должен быть экземпляром Product")
        self._items.append(product)

    def remove_by_id(self, product_id: int) -> bool:
        """Удалить товар по ID."""
        for idx in range(len(self._items)):
            if self._items[idx].id == product_id:
                self._items.pop(idx)
                return True
        return False

    def find_by_id(self, product_id: int):
        """Найти товар по ID."""
        for p in self._items:
            if p.id == product_id:
                return p
        return None

    def get_all_as_tuple(self) -> tuple:
        """Возврат товаров в виде кортежа (tuple)."""
        return tuple(self._items)

    def get_unique_categories_as_set(self) -> set:
        """Возврат уникальных категорий в виде множества (set)."""
        cats = list()
        for p in self._items:
            cats.append(p.category)
        return set(cats)

    def count(self) -> int:
        return len(self._items)

    # --- Статические методы для аналитики и фильтрации ---

    @staticmethod
    def calculate_total_value(products: list) -> float:
        """Рассчитать общую стоимость всех складских запасов (@staticmethod)."""
        total = 0.0
        for p in products:
            total += p.price * p.quantity
        return round(total, 2)

    @staticmethod
    def calculate_total_quantity(products: list) -> int:
        """Рассчитать общее количество единиц на складе (@staticmethod)."""
        qty = 0
        for p in products:
            qty += p.quantity
        return qty

    @staticmethod
    def filter_products(
        products: list,
        query: str,
        category: str,
        in_stock_only: bool,
    ) -> list:
        """Фильтрация товаров по критериям (@staticmethod)."""
        filtered = list()
        search_query = query.strip().lower()

        for p in products:
            if search_query:
                name_match = search_query in p.name.lower()
                barcode_match = search_query in p.barcode.lower()
                desc_match = search_query in p.description.lower()
                if not (name_match or barcode_match or desc_match):
                    continue

            if category and category != "Все категории":
                if p.category != category:
                    continue

            if in_stock_only and not bool(p):
                continue

            filtered.append(p)
        return filtered

    @staticmethod
    def create_initial_dataset() -> list:
        """
        Создать начальный набор из более чем 10 пользовательских объектов Product (@staticmethod).
        Требование: не менее 10 пользовательских объектов.
        """
        catalog = list()
        catalog.append(
            Product(
                101,
                "Ноутбук ThinkPad T14",
                "Электроника",
                89990.00,
                15,
                "4601234567890",
                4.8,
                "Надежный корпоративный ноутбук на процессоре AMD Ryzen 7 PRO",
            )
        )
        catalog.append(
            Product(
                102,
                "Монитор UltraSharp 27 4K",
                "Электроника",
                45500.50,
                8,
                "4601234567891",
                4.9,
                "Профессиональный IPS монитор с точной цветопередачей 99% sRGB",
            )
        )
        catalog.append(
            Product(
                103,
                "Механическая клавиатура Keychron K2",
                "Периферия",
                8490.00,
                24,
                "4601234567892",
                4.7,
                "Беспроводная механическая клавиатура с переключателями Gateron Brown",
            )
        )
        catalog.append(
            Product(
                104,
                "Беспроводная мышь MX Master 3S",
                "Периферия",
                9990.00,
                30,
                "4601234567893",
                4.9,
                "Эргономичная мышь с электромагнитным колесом прокрутки MagSpeed",
            )
        )
        catalog.append(
            Product(
                105,
                "Гарнитура HyperX Cloud II",
                "Аудио",
                7990.00,
                12,
                "4601234567894",
                4.6,
                "Игровая гарнитура с виртуальным объемным звуком 7.1",
            )
        )
        catalog.append(
            Product(
                106,
                "Студийный микрофон Shure MV7",
                "Аудио",
                26500.00,
                5,
                "4601234567895",
                4.9,
                "Динамический гибридный USB/XLR микрофон для подкастов и стримов",
            )
        )
        catalog.append(
            Product(
                107,
                "Внешний SSD Samsung T7 1TB",
                "Хранение данных",
                11990.00,
                18,
                "4601234567896",
                4.8,
                "Портативный твердотельный накопитель со скоростью до 1050 МБ/с",
            )
        )
        catalog.append(
            Product(
                108,
                "Маршрутизатор Wi-Fi 6 AX3000",
                "Сетевое оборудование",
                6290.00,
                14,
                "4601234567897",
                4.5,
                "Двухдиапазонный гигабитный роутер стандарта 802.11ax",
            )
        )
        catalog.append(
            Product(
                109,
                "Сетевое хранилище NAS 2-Bay",
                "Сетевое оборудование",
                32000.00,
                4,
                "4601234567898",
                4.7,
                "Компактный сервер для резервного копирования и медиабиблиотеки",
            )
        )
        catalog.append(
            Product(
                110,
                "Веб-камера 4K Pro Stream",
                "Периферия",
                14500.00,
                0,
                "4601234567899",
                4.4,
                "Камера с автофокусом и поддержкой HDR для видеоконференций",
            )
        )
        catalog.append(
            Product(
                111,
                "Кабель USB-C Thunderbolt 4 1m",
                "Аксессуары",
                2490.00,
                50,
                "4601234567810",
                4.8,
                "Высокоскоростной кабель передачи данных до 40 Гбит/с и зарядки 100W",
            )
        )
        catalog.append(
            Product(
                112,
                "Источник бесперебойного питания 1500VA",
                "Питание",
                18900.00,
                6,
                "4601234567811",
                4.6,
                "Линейно-интерактивный ИБП с LCD-дисплеем и защитой от перепадов",
            )
        )
        return catalog
