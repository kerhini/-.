"""Классы предметной области: товар, репозиторий, базовая сущность."""

from abc import ABC, abstractmethod


class BaseEntity(ABC):
    """Абстрактный базовый класс для сущностей приложения."""

    @abstractmethod
    def get_id(self) -> int:
        pass

    @abstractmethod
    def get_display_name(self) -> str:
        pass

    @abstractmethod
    def validate(self) -> bool:
        pass

    @abstractmethod
    def to_row(self) -> list:
        pass


class Product(BaseEntity):
    """Товарная позиция складского каталога."""

    def __init__(self, product_id: int, name: str, category: str,
                 price: float, quantity: int, barcode: str,
                 rating: float, description: str):
        self._id = 0
        self._name = ""
        self._category = ""
        self._price = 0.0
        self._quantity = 0
        self._barcode = ""
        self._rating = 0.0
        self._description = ""

        self.id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity
        self.barcode = barcode
        self.rating = rating
        self.description = description

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        if not isinstance(value, int) or value < 0:
            raise ValueError("ID должен быть неотрицательным целым числом")
        self._id = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Наименование не может быть пустым")
        self._name = value.strip()

    @property
    def category(self) -> str:
        return self._category

    @category.setter
    def category(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Категория не может быть пустой")
        self._category = value.strip()

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float):
        num_val = float(value)
        if num_val < 0.0:
            raise ValueError("Цена не может быть отрицательной")
        self._price = round(num_val, 2)

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int):
        int_val = int(value)
        if int_val < 0:
            raise ValueError("Количество не может быть отрицательным")
        self._quantity = int_val

    @property
    def barcode(self) -> str:
        return self._barcode

    @barcode.setter
    def barcode(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Штрихкод должен быть строкой")
        self._barcode = value.strip()

    @property
    def rating(self) -> float:
        return self._rating

    @rating.setter
    def rating(self, value: float):
        num_val = float(value)
        if num_val < 0.0 or num_val > 5.0:
            raise ValueError("Рейтинг должен быть в диапазоне 0.0–5.0")
        self._rating = round(num_val, 1)

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Описание должно быть строкой")
        self._description = value.strip()

    def get_id(self) -> int:
        return self._id

    def get_display_name(self) -> str:
        return self._name

    def validate(self) -> bool:
        return (
            self._id >= 0
            and len(self._name) > 0
            and len(self._category) > 0
            and self._price >= 0.0
            and self._quantity >= 0
            and (0.0 <= self._rating <= 5.0)
        )

    def to_row(self) -> list:
        return [
            str(self._id),
            self._name,
            self._category,
            f"{self._price:,.2f} руб.",
            str(self._quantity),
            self._barcode,
            f"{self._rating:.1f} \u2605",
        ]

    def __repr__(self) -> str:
        return (
            f"Product(id={self._id}, name={self._name!r}, "
            f"category={self._category!r}, price={self._price}, "
            f"quantity={self._quantity})"
        )

    def __str__(self) -> str:
        return (
            f"Товар №{self._id}: '{self._name}' ({self._category}) — "
            f"{self._price:.2f} руб. [{self._quantity} шт.]"
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, Product):
            return False
        return self._id == other._id and self._barcode == other._barcode

    def __lt__(self, other) -> bool:
        if not isinstance(other, Product):
            return NotImplemented
        if self._price != other._price:
            return self._price < other._price
        return self._id < other._id

    def __gt__(self, other) -> bool:
        if not isinstance(other, Product):
            return NotImplemented
        if self._price != other._price:
            return self._price > other._price
        return self._id > other._id

    def __le__(self, other) -> bool:
        if not isinstance(other, Product):
            return NotImplemented
        return self < other or self == other

    def __ge__(self, other) -> bool:
        if not isinstance(other, Product):
            return NotImplemented
        return self > other or self == other

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash((self._id, self._barcode))

    def __bool__(self) -> bool:
        return self._quantity > 0

    def __float__(self) -> float:
        return float(self._price)

    def __int__(self) -> int:
        return int(self._quantity)

    def __len__(self) -> int:
        return len(self._description)


class ProductRepository:
    """Репозиторий товаров: хранение, поиск, фильтрация, аналитика."""

    def __init__(self):
        self._items = list()

    @property
    def items(self) -> list:
        return self._items

    @items.setter
    def items(self, new_items: list):
        if not isinstance(new_items, list):
            raise TypeError("Ожидается list")
        self._items = new_items

    def add(self, product: Product):
        if not isinstance(product, Product):
            raise TypeError("Объект должен быть экземпляром Product")
        self._items.append(product)

    def remove_by_id(self, product_id: int) -> bool:
        for idx in range(len(self._items)):
            if self._items[idx].id == product_id:
                self._items.pop(idx)
                return True
        return False

    def find_by_id(self, product_id: int):
        for p in self._items:
            if p.id == product_id:
                return p
        return None

    def get_all_as_tuple(self) -> tuple:
        return tuple(self._items)

    def get_unique_categories_as_set(self) -> set:
        return set(p.category for p in self._items)

    def count(self) -> int:
        return len(self._items)

    @staticmethod
    def calculate_total_value(products: list) -> float:
        total = 0.0
        for p in products:
            total += p.price * p.quantity
        return round(total, 2)

    @staticmethod
    def calculate_total_quantity(products: list) -> int:
        qty = 0
        for p in products:
            qty += p.quantity
        return qty

    @staticmethod
    def filter_products(products: list, query: str,
                        category: str, in_stock_only: bool) -> list:
        filtered = list()
        q = query.strip().lower()
        for p in products:
            if q and not (q in p.name.lower() or
                          q in p.barcode.lower() or
                          q in p.description.lower()):
                continue
            if category and category != "Все категории" and p.category != category:
                continue
            if in_stock_only and not bool(p):
                continue
            filtered.append(p)
        return filtered

    @staticmethod
    def create_initial_dataset() -> list:
        """Создать начальный набор товаров."""
        return [
            Product(101, "Ноутбук ThinkPad T14", "Электроника",
                    89990.00, 15, "4601234567890", 4.8,
                    "Корпоративный ноутбук на AMD Ryzen 7 PRO"),
            Product(102, "Монитор UltraSharp 27 4K", "Электроника",
                    45500.50, 8, "4601234567891", 4.9,
                    "Профессиональный IPS монитор, 99% sRGB"),
            Product(103, "Механическая клавиатура Keychron K2", "Периферия",
                    8490.00, 24, "4601234567892", 4.7,
                    "Беспроводная клавиатура с переключателями Gateron Brown"),
            Product(104, "Беспроводная мышь MX Master 3S", "Периферия",
                    9990.00, 30, "4601234567893", 4.9,
                    "Эргономичная мышь с колесом прокрутки MagSpeed"),
            Product(105, "Гарнитура HyperX Cloud II", "Аудио",
                    7990.00, 12, "4601234567894", 4.6,
                    "Игровая гарнитура с объёмным звуком 7.1"),
            Product(106, "Студийный микрофон Shure MV7", "Аудио",
                    26500.00, 5, "4601234567895", 4.9,
                    "Гибридный USB/XLR микрофон для подкастов"),
            Product(107, "Внешний SSD Samsung T7 1TB", "Хранение данных",
                    11990.00, 18, "4601234567896", 4.8,
                    "Портативный накопитель до 1050 МБ/с"),
            Product(108, "Маршрутизатор Wi-Fi 6 AX3000", "Сетевое оборудование",
                    6290.00, 14, "4601234567897", 4.5,
                    "Двухдиапазонный гигабитный роутер 802.11ax"),
            Product(109, "Сетевое хранилище NAS 2-Bay", "Сетевое оборудование",
                    32000.00, 4, "4601234567898", 4.7,
                    "Компактный сервер резервного копирования"),
            Product(110, "Веб-камера 4K Pro Stream", "Периферия",
                    14500.00, 0, "4601234567899", 4.4,
                    "Камера с автофокусом и HDR для видеоконференций"),
            Product(111, "Кабель USB-C Thunderbolt 4 1m", "Аксессуары",
                    2490.00, 50, "4601234567810", 4.8,
                    "Кабель 40 Гбит/с, зарядка 100W"),
            Product(112, "Источник бесперебойного питания 1500VA", "Питание",
                    18900.00, 6, "4601234567811", 4.6,
                    "Линейно-интерактивный ИБП с LCD-дисплеем"),
        ]
