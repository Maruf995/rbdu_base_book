from django.urls import path, include
from . import views

urlpatterns = [
    # Главная страница для читателей (с поисковиком)
    path('', views.reader_home, name='reader_home'),
    
    # Результаты поиска (каталог) и детальное окно  
    path('search/', views.book_list, name='book_list'),
    path('book/detail/<int:pk>/', views.book_detail, name='book_detail'),    
    path('address/add/', views.add_address, name='add_address'),
    # Секретные действия библиотекаря
    path('book/add/', views.book_create, name='book_create'),
    path('book/<int:pk>/update/', views.book_update, name='book_update'),
    path('book/<int:pk>/delete/', views.book_delete, name='book_delete'),
    path('section/add/', views.add_section, name='add_section'),
    path('export/excel/', views.export_books_excel, name='export_books_excel'),
    
    # Встроенные страницы Django для логина/выхода (login, logout)
    path('accounts/', include('django.contrib.auth.urls')),
]