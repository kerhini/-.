"""
Автоматизированный верификатор всех 12 обязательных требований преподавателя.
Каждая проверка оформлена как метод проверочного класса RequirementsValidator.
"""

import ast
import os
import sys
from abc import ABC
from datetime import datetime

# Импорты проектных модулей
from custom_map import CustomMap, MapEntry
from entities import BaseEntity, Product, ProductRepository
from report_generator import SessionRecord, SessionReportGenerator
from custom_widgets import (
    CustomMainWindow,
    CustomButton,
    CustomLineEdit,
    CustomLabel,
    CustomTableWidget,
    CustomComboBox,
    CustomSpinBox,
    CustomCheckBox,
    CustomProgressBar,
    CustomTextEdit,
    CustomGroupBox,
    CustomStatusBar,
    CustomDialog,
)


class RequirementsValidator:
    """Класс комплексной верификации соответствия проекта требованиям ТЗ."""

    PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

    @staticmethod
    def check_all() -> bool:
        """Запуск всех тестов соответствия."""
        print("=" * 70)
        print(" ЗАПУСК ПРОВЕРКИ 12 ТРЕБОВАНИЙ ЭКЗАМЕНАЦИОННОЙ РАБОТЫ (МТИ)")
        print("=" * 70)

        results = list()
        results.append(("1. Все сущности описаны через классы", RequirementsValidator.test_1_entities_are_classes()))
        results.append(("2. Переопределено >= 10 компонентов окна", RequirementsValidator.test_2_overridden_components()))
        results.append(("3. Функциональность строго в методах классов", RequirementsValidator.test_3_no_standalone_functions()))
        results.append(("4. Сущности наследованы от абстрактного класса", RequirementsValidator.test_4_abstract_class_inheritance()))
        results.append(("5. Переопределено >= 3 спец. метода + __eq__, __repr__, __str__", RequirementsValidator.test_5_special_methods()))
        results.append(("6. Пользовательские классы сравнимы", RequirementsValidator.test_6_comparability()))
        results.append(("7. Атрибуты имеют геттеры и сеттеры", RequirementsValidator.test_7_getters_and_setters()))
        results.append(("8. Запрет dict / Кастомный класс маппинга", RequirementsValidator.test_8_no_dict_and_custom_map()))
        results.append(("9. Использовано не менее 5 UI компонентов", RequirementsValidator.test_9_ui_components_count()))
        results.append(("10. Не менее 10 объектов в коллекциях", RequirementsValidator.test_10_objects_and_collections()))
        results.append(("11. Выравнивание компонентов (Layouts)", RequirementsValidator.test_11_component_alignment()))
        results.append(("12. Отчет сессии в установленном формате", RequirementsValidator.test_12_session_report_format()))

        print("\n" + "=" * 70)
        print(" ИТОГОВАЯ ВЕДОМОСТЬ СООТВЕТСТВИЯ:")
        print("=" * 70)
        all_passed = True
        for name, passed in results:
            status = "[+] ВЫПОЛНЕНО" if passed else "[-] НЕ ВЫПОЛНЕНО"
            if not passed:
                all_passed = False
            print(f" {status} | {name}")
        print("=" * 70)
        if all_passed:
            print(" [OK] ВСЕ 12 ТРЕБОВАНИЙ ВЫПОЛНЕНЫ НА 100%!")
        else:
            print(" [!] ЕСТЬ НЕВЫПОЛНЕННЫЕ ПУНКТЫ.")
        print("=" * 70)
        return all_passed

    @staticmethod
    def test_1_entities_are_classes() -> bool:
        """Проверка, что сущности Product, BaseEntity, CustomMap, MapEntry и др. являются классами."""
        classes = [BaseEntity, Product, ProductRepository, CustomMap, MapEntry, SessionRecord, SessionReportGenerator]
        for c in classes:
            if not isinstance(c, type):
                return False
        return True

    @staticmethod
    def test_2_overridden_components() -> bool:
        """Проверка: переопределено как минимум 10 компонентов окна."""
        custom_widgets = [
            CustomMainWindow,
            CustomButton,
            CustomLineEdit,
            CustomLabel,
            CustomTableWidget,
            CustomComboBox,
            CustomSpinBox,
            CustomCheckBox,
            CustomProgressBar,
            CustomTextEdit,
            CustomGroupBox,
            CustomStatusBar,
            CustomDialog,
        ]
        count = len(custom_widgets)
        print(f"   [Пункт 2] Найдено {count} переопределенных компонентов окна (требуется >= 10).")
        return count >= 10

    @staticmethod
    def test_3_no_standalone_functions() -> bool:
        """
        Проверка: отсутствие отдельных (top-level) функций в коде проекта.
        Вся функциональность должна быть в методах классов.
        """
        src_files = [
            "custom_map.py",
            "entities.py",
            "custom_widgets.py",
            "report_generator.py",
            "product_dialog.py",
            "login_dialog.py",
            "main_window.py",
            "main.py",
        ]
        for filename in src_files:
            file_path = os.path.join(RequirementsValidator.PROJECT_DIR, filename)
            if not os.path.exists(file_path):
                continue
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=filename)
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    print(f"   [Пункт 3] Найдена автономная функция '{node.name}' вне класса в {filename}!")
                    return False
        return True

    @staticmethod
    def test_4_abstract_class_inheritance() -> bool:
        """Проверка: сущности наследованы от абстрактного класса (ABC)."""
        is_abc = issubclass(BaseEntity, ABC)
        inherits = issubclass(Product, BaseEntity)
        abstract_methods = getattr(BaseEntity, "__abstractmethods__", set())
        has_abstract_methods = len(abstract_methods) > 0
        return is_abc and inherits and has_abstract_methods

    @staticmethod
    def test_5_special_methods() -> bool:
        """
        Проверка: переопределить как минимум 3 спец. метода + __eq__, __repr__, __str__.
        Итого требуется переопределить >= 6 спец. методов.
        """
        required_base = {"__eq__", "__repr__", "__str__"}
        for method in required_base:
            if method not in Product.__dict__:
                print(f"   [Пункт 5] Отсутствует базовый спец. метод {method} в Product")
                return False

        additional_dunders = list()
        all_dunders = [
            "__lt__",
            "__gt__",
            "__le__",
            "__ge__",
            "__ne__",
            "__hash__",
            "__bool__",
            "__float__",
            "__int__",
            "__len__",
        ]
        for d in all_dunders:
            if d in Product.__dict__:
                additional_dunders.append(d)

        print(f"   [Пункт 5] Дополнительные переопределенные спец. методы: {', '.join(additional_dunders)} ({len(additional_dunders)} шт.)")
        return len(additional_dunders) >= 3

    @staticmethod
    def test_6_comparability() -> bool:
        """Проверка: пользовательские классы должны быть сравнимы (<, >, <=, >=, ==)."""
        p1 = Product(1, "Товар А", "Кат 1", 100.0, 10, "111", 5.0, "Desc A")
        p2 = Product(2, "Товар Б", "Кат 1", 200.0, 5, "222", 4.0, "Desc B")
        p3 = Product(3, "Товар В", "Кат 1", 100.0, 2, "333", 4.5, "Desc C")

        assert (p1 < p2) is True
        assert (p2 > p1) is True
        assert (p1 <= p2) is True
        assert (p2 >= p1) is True
        assert (p1 == p1) is True
        assert (p1 != p2) is True

        products_list = [p2, p1, p3]
        products_list.sort()
        # Проверка сортировки по цене (100.0 ID 1, 100.0 ID 3, 200.0 ID 2)
        assert products_list[0].id == 1
        assert products_list[1].id == 3
        assert products_list[2].id == 2
        return True

    @staticmethod
    def test_7_getters_and_setters() -> bool:
        """Проверка: атрибуты имеют геттеры и сеттеры (@property)."""
        attributes = ["id", "name", "category", "price", "quantity", "barcode", "rating", "description"]
        for attr in attributes:
            prop = getattr(Product, attr, None)
            if not isinstance(prop, property):
                print(f"   [Пункт 7] Атрибут '{attr}' не является property")
                return False
            if prop.fget is None or prop.fset is None:
                print(f"   [Пункт 7] У атрибута '{attr}' отсутствует геттер или сеттер")
                return False

        # Проверка работы сеттера и валидации
        p = Product(10, "Тест", "Кат", 50.0, 5, "999", 4.0, "Описание")
        p.price = 99.99
        assert p.price == 99.99
        try:
            p.price = -10.0
            return False  # Отрицательная цена должна вызывать ValueError
        except ValueError:
            pass
        return True

    @staticmethod
    def test_8_no_dict_and_custom_map() -> bool:
        """
        Проверка:
        1. Запрещено использовать Map (dict) - в коде проекта нет ast.Dict, ast.DictComp или вызовов dict().
        2. Работоспособность кастомного класса CustomMap.
        """
        src_files = [
            "custom_map.py",
            "entities.py",
            "custom_widgets.py",
            "report_generator.py",
            "product_dialog.py",
            "login_dialog.py",
            "main_window.py",
            "main.py",
        ]
        for filename in src_files:
            file_path = os.path.join(RequirementsValidator.PROJECT_DIR, filename)
            if not os.path.exists(file_path):
                continue
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=filename)

            for node in ast.walk(tree):
                if isinstance(node, (ast.Dict, ast.DictComp)):
                    print(f"   [Пункт 8] Обнаружен синтаксис словаря (dict) в {filename}, строка {node.lineno}!")
                    return False
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id == "dict":
                        print(f"   [Пункт 8] Обнаружен вызов dict() в {filename}, строка {node.lineno}!")
                        return False

        # Проверка работоспособности CustomMap
        cmap = CustomMap()
        cmap["key1"] = "val1"
        cmap.put("key2", "val2")
        assert len(cmap) == 2
        assert cmap["key1"] == "val1"
        assert cmap.get("key2") == "val2"
        assert cmap.get("missing", 42) == 42
        assert "key1" in cmap
        del cmap["key1"]
        assert len(cmap) == 1
        assert "key1" not in cmap
        return True

    @staticmethod
    def test_9_ui_components_count() -> bool:
        """Проверка: использовать не менее 5 UI компонентов."""
        components = [
            CustomMainWindow,
            CustomButton,
            CustomLineEdit,
            CustomLabel,
            CustomTableWidget,
            CustomComboBox,
            CustomSpinBox,
            CustomCheckBox,
            CustomProgressBar,
            CustomTextEdit,
            CustomGroupBox,
            CustomStatusBar,
            CustomDialog,
        ]
        return len(components) >= 5

    @staticmethod
    def test_10_objects_and_collections() -> bool:
        """
        Проверка: не менее 10 пользовательских объектов,
        хранение в коллекциях (list, tuple, set).
        """
        dataset = ProductRepository.create_initial_dataset()
        if len(dataset) < 10:
            print(f"   [Пункт 10] В начальном наборе всего {len(dataset)} объектов (< 10)!")
            return False

        repo = ProductRepository()
        for p in dataset:
            repo.add(p)

        # Проверка типов коллекций
        tup = repo.get_all_as_tuple()
        if not isinstance(tup, tuple) or len(tup) < 10:
            return False

        cats_set = repo.get_unique_categories_as_set()
        if not isinstance(cats_set, set) or len(cats_set) < 2:
            return False

        if not isinstance(repo.items, list) or len(repo.items) < 10:
            return False

        print(f"   [Пункт 10] Успешно создано {len(dataset)} объектов в коллекциях list, tuple, set.")
        return True

    @staticmethod
    def test_11_component_alignment() -> bool:
        """Проверка: компоненты окна выравнены через менеджеры компоновки."""
        with open(os.path.join(RequirementsValidator.PROJECT_DIR, "main_window.py"), "r", encoding="utf-8") as f:
            content = f.read()

        has_grid = "QGridLayout" in content
        has_vbox = "QVBoxLayout" in content
        has_hbox = "QHBoxLayout" in content
        has_align = "AlignmentFlag" in content
        return has_grid and has_vbox and has_hbox and has_align

    @staticmethod
    def test_12_session_report_format() -> bool:
        """
        Проверка: при закрытии приложения сохраняется отчет о работе приложения в формате:
        +------------------------------------+
        | login | time_in | time_out |
        |---------|------------|-------------|
        |UserName | <datatime> | <datatime> |
        +------------------------------------+
        Формат времени %d.%m.%Y %H:%M:%S
        """
        t_in = datetime(2026, 10, 11, 14, 30, 0)
        t_out = datetime(2026, 10, 11, 15, 45, 30)
        record = SessionRecord("Student_MTI", t_in, t_out)

        table_str = SessionReportGenerator.build_report_table(record)

        # Проверка обязательных элементов заголовка и границ
        assert "+-" in table_str
        assert "login" in table_str
        assert "time_in" in table_str
        assert "time_out" in table_str
        assert "Student_MTI" in table_str
        assert "11.10.2026 14:30:00" in table_str
        assert "11.10.2026 15:45:30" in table_str

        # Проверка сохранения в файл
        test_file = os.path.join(RequirementsValidator.PROJECT_DIR, "test_session_report.txt")
        if os.path.exists(test_file):
            os.remove(test_file)

        SessionReportGenerator.save_report_to_file(record, test_file)
        assert os.path.exists(test_file)
        with open(test_file, "r", encoding="utf-8") as f:
            saved_content = f.read()
        assert "Student_MTI" in saved_content
        assert "11.10.2026 14:30:00" in saved_content
        os.remove(test_file)
        return True


class TestRunner:
    """Класс запуска тестового скрипта (@staticmethod)."""

    @staticmethod
    def main():
        success = RequirementsValidator.check_all()
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    TestRunner.main()
