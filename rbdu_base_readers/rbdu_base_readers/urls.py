from django.contrib import admin
from django.urls import path, include  # <-- ВАЖНО: добавили импорт include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Подключаем маршруты вашего приложения к главной странице.
    # Замените 'ваше_приложение' на реальное название папки с приложением 
    # (скорее всего это 'catalog' или 'readers')
    path('', include('catalog.urls')),
]