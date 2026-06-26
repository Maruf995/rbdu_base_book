import random
from catalog.models import Book, Section, Address

print("Начало генерации тестовых данных...")

# 1. Базовые отрасли знаний для библиотеки
section_names = [
    "Художественная литература", 
    "История и география", 
    "Технические науки", 
    "Естественные науки", 
    "Психология и философия", 
    "Языкознание и словари"
]
sections = [Section.objects.get_or_create(name=name)[0] for name in section_names]


# ИСПРАВЛЕНИЕ: Автоматически создаем или находим объекты Address в базе данных
address_names = [
    "Стеллаж 1, Полка A", 
    "Стеллаж 2, Полка B", 
    "Читальный зал, Шкаф 3", 
    "Фонд хранения, Сектор 4", 
    "Абонемент, Полка 5", 
    "Стеллаж 4, Полка Г"
]
addresses = [Address.objects.get_or_create(name=name)[0] for name in address_names]


# 2. Наборы данных для генерации случайных книг
authors = ["Ч. Айтматов", "А. Пушкин", "Л. Толстой", "Ф. Достоевский", "Дж. Оруэлл", "С. Кинг", "А. Кристи", "М. Булгаков", "Э. М. Ремарк", "Х. Мураками", "Р. Брэдбери"]

# Элементы для сборных художественных названий
adjectives = ["Белый", "Черный", "Великий", "Тайный", "Древний", "Последний", "Новый", "Золотой", "Ночной", "Вечный", "Забытый"]
nouns = ["пароход", "замок", "путь", "человек", "век", "город", "дневник", "остров", "мир", "свет", "океан"]

# Готовые научные/учебные заглавия
scientific_titles = ["Основы физики", "История Кыргызстана", "Алгоритмы на Python", "Высшая математика", "Психология общения", "Введение в философию", "Общая химия", "Экономическая теория"]

letters = ["А", "Б", "В", "Г", "Д", "К", "М", "Н", "Т", "Х", "У"]
notes = ["", "", "", "Подарочное издание", "Новое поступление", "Редкий экземпляр", "Требует переплета"]


# 3. Безопасный расчет инвентарных номеров
last_book = Book.objects.all().order_by('-id').first()
try:
    start_inv = int(last_book.inventory_number) + 1 if last_book and last_book.inventory_number.isdigit() else 10000
except ValueError:
    start_inv = 10000


# 4. Оптимизированный цикл создания уникальных книг
total_records = 100000
batch_size = 5000  # Размер пачки для сохранения в БД одним махом
books_to_create = []
created_count = 0

for i in range(total_records):
    current_inv_num = start_inv + i

    # УНИКАЛЬНОСТЬ: Добавляем уникальное число в скобках к каждому названию книги
    if random.random() > 0.4:
        title = f"{random.choice(adjectives)} {random.choice(nouns)} (Изд. №{current_inv_num})"
        author = random.choice(authors)
    else:
        title = f"{random.choice(scientific_titles)} (Том {random.randint(1, 4)}, Выпуск {current_inv_num})"
        author = "Сборник авторов" if random.random() > 0.6 else random.choice(authors)

    inv_num = str(current_inv_num)
    cipher = f"{random.choice(letters)}-{random.randint(10, 99)}/{random.randint(1, 9)}"
    year = random.randint(1960, 2026) 
    address = random.choice(addresses)  # ТЕПЕРЬ ТУТ СЛУЧАЙНЫЙ ОБЪЕКТ ADDRESS (НЕ СТРОКА!)
    cost = random.randint(150, 3500)
    section = random.choice(sections)
    note = random.choice(notes)

    # Вместо записи в БД, просто собираем объекты в список в оперативной памяти
    books_to_create.append(
        Book(
            inventory_number=inv_num,
            cipher=cipher,
            author=author,
            title=title,
            section=section,
            publication_year=year,
            address=address,
            cost=cost,
            note=note
        )
    )
    created_count += 1

    # Как только накопилось 5000 книг — выстреливаем ими в базу данных одним запросом
    if len(books_to_create) >= batch_size:
        Book.objects.bulk_create(books_to_create)
        books_to_create = []  # Очищаем список для следующей пачки
        print(f"Сгенерировано и записано: {created_count} из {total_records} книг...")

# Если в конце цикла остались книги, которые не вошли в ровную пачку — догружаем их
if books_to_create:
    Book.objects.bulk_create(books_to_create)

print(f"\nУра! В базу успешно добавлено {created_count} абсолютно УНИКАЛЬНЫХ книг.")