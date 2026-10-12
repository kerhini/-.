from abc import ABC, abstractmethod


# Базовый абстрактный класс для сущностей (требование по ООП)
class BaseEntity(ABC):

    @abstractmethod
    def get_id(self):
        pass

    @abstractmethod
    def get_display_name(self):
        pass

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def to_row(self):
        pass


# Класс товара на складе
class Product(BaseEntity):

    def __init__(self, product_id, name, category, price, quantity, barcode, rating, description):
        # Начальные значения полей
        self._id = 0
        self._name = ""
        self._category = ""
        self._price = 0.0
        self._quantity = 0
        self._barcode = ""
        self._rating = 0.0
        self._description = ""

        # Присваиваем через свойства для валидации
        self.id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity
        self.barcode = barcode
        self.rating = rating
        self.description = description

    # Свойство: ID товара
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        val = int(value)
        if val < 0:
            raise ValueError("ID товара не может быть меньше 0")
        self._id = val

    # Свойство: Название товара
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        val = str(value).strip()
        if not val:
            raise ValueError("Название товара не может быть пустым")
        self._name = val

    # Свойство: Категория
    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        val = str(value).strip()
        if not val:
            raise ValueError("Категория товара не может быть пустой")
        self._category = val

    # Свойство: Цена
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        val = float(value)
        if val < 0.0:
            raise ValueError("Цена товара не может быть отрицательной")
        self._price = round(val, 2)

    # Свойство: Количество на складе
    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        val = int(value)
        if val < 0:
            raise ValueError("Количество не может быть меньше 0")
        self._quantity = val

    # Свойство: Штрихкод
    @property
    def barcode(self):
        return self._barcode

    @barcode.setter
    def barcode(self, value):
        self._barcode = str(value).strip()

    # Свойство: Рейтинг
    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        val = float(value)
        if val < 0.0 or val > 5.0:
            raise ValueError("Рейтинг должен быть в пределах от 0 до 5")
        self._rating = round(val, 1)

    # Свойство: Описание товара
    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = str(value).strip()

    # Реализуем методы абстрактного класса
    def get_id(self):
        return self._id

    def get_display_name(self):
        return self._name

    def validate(self):
        if self._id < 0:
            return False
        if not self._name or not self._category:
            return False
        if self._price < 0 or self._quantity < 0:
            return False
        if self._rating < 0 or self._rating > 5:
            return False
        return True

    def to_row(self):
        row = list()
        row.append(str(self._id))
        row.append(self._name)
        row.append(self._category)
        row.append(f"{self._price:,.2f} руб.")
        row.append(str(self._quantity))
        row.append(self._barcode)
        row.append(f"{self._rating:.1f}")
        return row

    # Магические методы
    def __repr__(self):
        return f"Product(id={self._id}, name={self._name!r}, price={self._price})"

    def __str__(self):
        return f"Товар №{self._id}: {self._name} ({self._price:.2f} руб.)"

    def __eq__(self, other):
        if not isinstance(other, Product):
            return False
        return self._id == other._id and self._barcode == other._barcode

    # Сравнение товаров: сначала по цене, потом по ID
    def __lt__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        if self._price != other._price:
            return self._price < other._price
        return self._id < other._id

    def __gt__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        if self._price != other._price:
            return self._price > other._price
        return self._id > other._id

    def __le__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        return self < other or self == other

    def __ge__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        return self > other or self == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self._id, self._barcode))

    def __bool__(self):
        # Есть ли товар в наличии
        return self._quantity > 0

    def __float__(self):
        return float(self._price)

    def __int__(self):
        return int(self._quantity)

    def __len__(self):
        return len(self._description)


# Репозиторий для хранения и обработки списка товаров
class ProductRepository:

    def __init__(self):
        self._items = list()

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, new_items):
        if not isinstance(new_items, list):
            raise TypeError("Ожидается список list")
        self._items = new_items

    # Добавить товар
    def add(self, product):
        if not isinstance(product, Product):
            raise TypeError("Ожидается объект Product")
        self._items.append(product)

    # Удалить товар по ID
    def remove_by_id(self, product_id):
        for i in range(len(self._items)):
            if self._items[i].id == product_id:
                self._items.pop(i)
                return True
        return False

    # Найти товар по ID
    def find_by_id(self, product_id):
        for prod in self._items:
            if prod.id == product_id:
                return prod
        return None

    # Вернуть товары в виде кортежа
    def get_all_as_tuple(self):
        return tuple(self._items)

    # Вернуть уникальные категории в виде множества
    def get_unique_categories_as_set(self):
        cats = set()
        for prod in self._items:
            cats.add(prod.category)
        return cats

    # Количество товаров
    def count(self):
        return len(self._items)

    # Подсчет общей стоимости всех товаров
    @staticmethod
    def calculate_total_value(products):
        total = 0.0
        for p in products:
            total += p.price * p.quantity
        return round(total, 2)

    # Подсчет общего количества единиц на складе
    @staticmethod
    def calculate_total_quantity(products):
        total = 0
        for p in products:
            total += p.quantity
        return total

    # Фильтрация списка товаров
    @staticmethod
    def filter_products(products, query, category, in_stock_only):
        result = list()
        q = query.strip().lower()

        for p in products:
            if q:
                in_name = q in p.name.lower()
                in_code = q in p.barcode.lower()
                in_desc = q in p.description.lower()
                if not (in_name or in_code or in_desc):
                    continue

            if category and category != "Все категории" and p.category != category:
                continue

            if in_stock_only and not bool(p):
                continue

            result.append(p)

        return result

    # Начальный каталог товаров
    @staticmethod
    def create_initial_dataset():
        catalog = list()
        catalog.append(Product(101, "Ноутбук ThinkPad T14", "Электроника", 89990.0, 15, "4601234567890", 4.8, "Надежный корпоративный ноутбук на процессоре AMD Ryzen 7 PRO"))
        catalog.append(Product(102, "Монитор UltraSharp 27 4K", "Электроника", 45500.5, 8, "4601234567891", 4.9, "Профессиональный IPS монитор с точной цветопередачей 99% sRGB"))
        catalog.append(Product(103, "Механическая клавиатура Keychron K2", "Периферия", 8490.0, 24, "4601234567892", 4.7, "Беспроводная механическая клавиатура с переключателями Gateron Brown"))
        catalog.append(Product(104, "Беспроводная мышь MX Master 3S", "Периферия", 9990.0, 30, "4601234567893", 4.9, "Эргономичная мышь с электромагнитным колесом прокрутки MagSpeed"))
        catalog.append(Product(105, "Гарнитура HyperX Cloud II", "Аудио", 7990.0, 12, "4601234567894", 4.6, "Игровая гарнитура с виртуальным объемным звуком 7.1"))
        catalog.append(Product(106, "Студийный микрофон Shure MV7", "Аудио", 26500.0, 5, "4601234567895", 4.9, "Динамический гибридный USB/XLR микрофон для подкастов и стримов"))
        catalog.append(Product(107, "Внешний SSD Samsung T7 1TB", "Хранение данных", 11990.0, 18, "4601234567896", 4.8, "Портативный твердотельный накопитель со скоростью до 1050 МБ/с"))
        catalog.append(Product(108, "Маршрутизатор Wi-Fi 6 AX3000", "Сетевое оборудование", 6290.0, 14, "4601234567897", 4.5, "Двухдиапазонный гигабитный роутер стандарта 802.11ax"))
        catalog.append(Product(109, "Сетевое хранилище NAS 2-Bay", "Сетевое оборудование", 32000.0, 4, "4601234567898", 4.7, "Компактный сервер для резервного копирования и медиабиблиотеки"))
        catalog.append(Product(110, "Веб-камера 4K Pro Stream", "Периферия", 14500.0, 0, "4601234567899", 4.4, "Камера с автофокусом и поддержкой HDR для видеоконференций"))
        catalog.append(Product(111, "Кабель USB-C Thunderbolt 4 1m", "Аксессуары", 2490.0, 50, "4601234567810", 4.8, "Высокоскоростной кабель передачи данных до 40 Гбит/с и зарядки 100W"))
        catalog.append(Product(112, "Источник бесперебойного питания 1500VA", "Питание", 18900.0, 6, "4601234567811", 4.6, "Линейно-интерактивный ИБП с LCD-дисплеем и защитой от перепадов"))
        return catalog
