import pytest
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.urls import reverse
from django.test import Client
# ВАЖНО: Замените 'your_app_name' на название вашего приложения
from catalog.models import Book, Section

# transaction=True обязателен для многопоточных тестов БД в Django
@pytest.mark.django_db(transaction=True)
class TestConcurrency:

    @pytest.fixture
    def setup_data(self):
        """Фикстура для создания начальных данных."""
        section = Section.objects.create(name="Научная литература")
        return section

    def test_concurrent_book_creation(self, setup_data):
        """
        Тест одновременного создания книг.
        Проверяет, не упадет ли БД от множества одновременных INSERT-запросов.
        """
        section = setup_data
        url = reverse('book_create')  # Убедитесь, что имя url совпадает с вашим urls.py
        
        # Функция, которая будет выполняться в каждом потоке
        def make_post_request(i):
            client = Client() # Обязательно создаем новый клиент для каждого потока
            data = {
                'inventory_number': f'INV-{i}',
                'title': f'Тестовая книга {i}',
                'author': 'Иван Иванов',
                'section': section.id,
                'cipher': f'123-{i}',
                'publication_year': 2023,
                'address': 'Стеллаж 1',
                'cost': 500
            }
            # Отправляем POST запрос
            response = client.post(url, data)
            return response.status_code

        # Запускаем 50 одновременных потоков
        concurrent_requests = 50
        status_codes = []
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            # Создаем пул задач
            futures = [executor.submit(make_post_request, i) for i in range(concurrent_requests)]
            
            # Собираем результаты по мере их выполнения
            for future in as_completed(futures):
                try:
                    status_codes.append(future.result())
                except Exception as e:
                    pytest.fail(f"Поток вызвал исключение: {e}")

        # Проверяем, что ни один запрос не завершился 500 ошибкой (Internal Server Error)
        assert 500 not in status_codes, "Обнаружено падение сервера (ошибка 500) при конкурентной записи!"
        
        # Проверяем, что все книги действительно создались (302 Redirect — это успешное создание в вашем коде)
        assert Book.objects.count() == concurrent_requests

    def test_concurrent_excel_export(self, setup_data):
        """
        Тест одновременной генерации Excel-файлов.
        Проверяет, не упадет ли сервер от одновременной нагрузки на процессор (openpyxl).
        """
        # Создадим несколько книг для экспорта
        for i in range(10):
            Book.objects.create(
                inventory_number=f'EX-{i}',
                title=f'Книга для экспорта {i}',
                section=setup_data
            )

        url = reverse('export_books_excel') # Убедитесь, что имя url совпадает с вашим urls.py

        def make_export_request():
            client = Client()
            response = client.get(url)
            return response.status_code

        concurrent_requests = 20
        status_codes = []

        # Запускаем одновременные GET-запросы на скачивание Excel
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_export_request) for _ in range(concurrent_requests)]
            
            for future in as_completed(futures):
                try:
                    status_codes.append(future.result())
                except Exception as e:
                    pytest.fail(f"Поток вызвал исключение при экспорте: {e}")

        # Проверяем, что все запросы успешно вернули файл (код 200)
        assert 500 not in status_codes, "Падение сервера при одновременной генерации Excel!"
        assert all(code == 200 for code in status_codes), "Не все запросы вернули статус 200."