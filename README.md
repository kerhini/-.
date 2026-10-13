# Warehouse Management System

Меню входа
<img width="341" height="189" alt="image" src="https://github.com/user-attachments/assets/4f9e1536-9a88-4377-9d66-e3b7163eb34b" />

Главное меню
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/6682e47f-6695-4e2d-b2fc-9ea807976b15" />

Отчет о сессии
<img width="361" height="236" alt="image" src="https://github.com/user-attachments/assets/df0be369-b2ee-40a8-b107-c074f9fbee49" />




Десктопное приложение для складского учёта и управления каталогом товаров с графическим интерфейсом на PyQt6.

## Возможности

- Каталог товаров с информацией о ценах, категориях, остатках и рейтинге
- Поиск по названию, коду и описанию
- Фильтрация по категориям и наличию товаров на складе
- Сортировка по стоимости и идентификатору
- Добавление, редактирование и удаление товаров
- Карточка выбранного товара с детальным описанием
- Сводная статистика по запасам и стоимости
- Автоматическая фиксация времени сессий в файл `session_report.txt`

## Установка и запуск

1. Установка зависимостей:
```bash
pip install PyQt6
```

2. Запуск приложения:
```bash
python main.py
```

## Структура проекта

- `main.py` — запуск приложения
- `main_window.py` — главное окно
- `entities.py` — модели данных (`Product`, `ProductRepository`)
- `custom_widgets.py` — компоненты графического интерфейса
- `custom_map.py` — ассоциативный массив
- `product_dialog.py` — форма редактирования товара
- `login_dialog.py` — окно входа
- `report_generator.py` — генерация отчёта о работе
