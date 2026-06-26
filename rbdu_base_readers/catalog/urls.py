from django.urls import path
from . import views

# Указываем имя приложения (namespace), чтобы работали ссылки вроде 'catalog:book_list'
app_name = 'catalog' 

urlpatterns = [
    # Главная страница читателя
    path('', views.reader_home, name='reader_home'),
    
    # Список всех книг (с поиском, фильтрацией и пагинацией)
    path('books/', views.book_list, name='book_list'),
    
    # Детальная страница конкретной книги
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
]