from abc import ABC, abstractmethod


# Базовый абстрактный класс для сущностей программы
class BaseEntity(ABC):

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


# Основной класс товара на складе
class Product(BaseEntity):

    def __init__(self, product_id: int, name: str, category: str,
                 price: float, quantity: int, barcode: str,
                 rating: float, description: str):
        # Инициализируем переменные через свойства для проверки данных
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

    # Геттеры и сеттеры
    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        val = int(value)
        if val < 0:
            raise ValueError("ID не может быть отрицательным")
        self._id = val

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        val = str(value).strip()
        if not val:
            raise ValueError("Название товара не может быть пустым")
        self._name = val

    @property
    def category(self) -> str:
        return self._category

    @category.setter
    def category(self, value: str):
        val = str(value).strip()
        if not val:
            raise ValueError("Категория не может быть пустой")
        self._category = val

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float):
        val = float(value)
        if val < 0.0:
            raise ValueError("Цена не может быть отрицательной")
        self._price = round(val, 2)

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int):
        val = int(value)
        if val < 0:
            raise ValueError("Количество не может быть отрицательным")
        self._quantity = val

    @property
    def barcode(self) -> str:
        return self._barcode

    @barcode.setter
    def barcode(self, value: str):
        self._barcode = str(value).strip()

    @property
    def rating(self) -> float:
        return self._rating

    @rating.setter
    def rating(self, value: float):
        val = float(value)
        if val < 0.0 or val > 5.0:
            raise ValueError("Рейтинг должен быть от 0 до 5")
        self._rating = round(val, 1)

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = str(value).strip()

    # Реализация методов базового абстрактного класса
    def get_id(self) -> int:
        return self._id

    def get_display_name(self) -> str:
        return self._name

    def validate(self) -> bool:
        if self._id < 0 or not self._name or not self._category:
            return False
        if self._price < 0 or self._quantity < 0:
            return False
        if self._rating < 0 or self._rating > 5:
            return False
        return True

    def to_row(self) -> list:
        # Формируем список ячеек для отображения в таблице
        return [
            str(self._id),
            self._name,
            self._category,
            f"{self._price:,.2f} руб.",
            str(self._quantity),
            self._barcode,
            f"{self._rating:.1f}",
        ]

    # Специальные методы
    def __repr__(self) -> str:
        return f"Product(id={self._id}, name={self._name!r}, price={self._price})"

    def __str__(self) -> str:
        return f"Товар #{self._id}: {self._name} - {self._price} руб."

    # Методы сравнения
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
        # Проверяем, есть ли товар в наличии
        return self._quantity > 0

    def __float__(self) -> float:
        return float(self._price)

    def __int__(self) -> int:
        return int(self._quantity)

    def __len__(self) -> int:
        # Длина описания товара
        return len(self._description)


# Класс для работы со списком товаров
class ProductRepository:

    def __init__(self):
        self._items = list()

    @property
    def items(self) -> list:
        return self._items

    @items.setter
    def items(self, new_items: list):
        if not isinstance(new_items, list):
            raise TypeError("Ожидается список list")
        self._items = new_items

    def add(self, product: Product):
        if not isinstance(product, Product):
            raise TypeError("Ожидается объект класса Product")
        self._items.append(product)

    def remove_by_id(self, product_id: int) -> bool:
        for i in range(len(self._items)):
            if self._items[i].id == product_id:
                self._items.pop(i)
                return True
        return False

    def find_by_id(self, product_id: int):
        for product in self._items:
            if product.id == product_id:
                return product
        return None

    def get_all_as_tuple(self) -> tuple:
        return tuple(self._items)

    def get_unique_categories_as_set(self) -> set:
        categories = set()
        for p in self._items:
            categories.add(p.category)
        return categories

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
        total = 0
        for p in products:
            total += p.quantity
        return total

    @staticmethod
    def filter_products(products: list, query: str, category: str, in_stock_only: bool) -> list:
        result = list()
        q = query.strip().lower()

        for p in products:
            # Поиск по подстроке в названии, описании или штрихкоде
            if q:
                in_name = q in p.name.lower()
                in_code = q in p.barcode.lower()
                in_desc = q in p.description.lower()
                if not (in_name or in_code or in_desc):
                    continue

            # Фильтр по категории
            if category and category != "Все категории" and p.category != category:
                continue

            # Фильтр только в наличии
            if in_stock_only and not bool(p):
                continue

            result.append(p)

        return result

    @staticmethod
    def create_initial_dataset() -> list:
        # Начальный список товаров для заполнения склада
        return [
            Product(101, "Ноутбук Lenovo IdeaPad", "Электроника",
                    48900.0, 12, "460010010001", 4.8,
                    "Ноутбук для работы и учебы, экран 15.6 дюймов"),
            Product(102, "Монитор Samsung 24", "Электроника",
                    14500.0, 8, "460010010002", 4.7,
                    "IPS монитор Full HD с тонкими рамками"),
            Product(103, "Беспроводная мышь Logitech", "Периферия",
                    1890.0, 30, "460010010003", 4.9,
                    "Оптическая мышь с удобным хватом"),
            Product(104, "Механическая клавиатура", "Периферия",
                    4200.0, 16, "460010010004", 4.6,
                    "Клавиатура с синей подсветкой и переключателями"),
            Product(105, "Наушники с микрофоном Sony", "Аудио",
                    3500.0, 10, "460010010005", 4.5,
                    "Накладные наушники с чистым звуком"),
            Product(106, "Настольный микрофон", "Аудио",
                    2900.0, 6, "460010010006", 4.4,
                    "USB микрофон с подставкой для записи и звонков"),
            Product(107, "Внешний SSD 512 ГБ", "Хранение данных",
                    5900.0, 15, "460010010007", 4.9,
                    "Скоростной портативный накопитель USB 3.2"),
            Product(108, "Wi-Fi роутер TP-Link", "Сетевое оборудование",
                    3100.0, 14, "460010010008", 4.6,
                    "Двухдиапазонный роутер для дома и офиса"),
            Product(109, "Веб-камера Full HD", "Периферия",
                    2400.0, 0, "460010010009", 4.2,
                    "Камера 1080p со встроенным микрофоном"),
            Product(110, "Сетевой фильтр 5 розеток", "Питание",
                    850.0, 45, "460010010010", 4.7,
                    "Удлинитель с защитой от перепадов напряжения 3м"),
            Product(111, "Кабель HDMI 1.8м", "Аксессуары",
                    390.0, 60, "460010010011", 4.8,
                    "Экранированный кабель для передачи видео"),
            Product(112, "Колонки 2.0 Sven", "Аудио",
                    1650.0, 11, "460010010012", 4.3,
                    "Компактная акустика с питанием от USB"),
        ]
