from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Book, Section, Address  # ИМПОРТИРУЕМ Address

# Регистрируем Разделы
@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# ДОБАВЛЯЕМ: Регистрируем Местонахождения (Адреса)
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Регистрируем Книги
@admin.register(Book)
class BookAdmin(ImportExportModelAdmin):
    # Добавили 'address' в list_display, чтобы видеть местонахождение прямо в таблице
    list_display = ('inventory_number', 'title', 'author', 'section', 'address', 'publication_year')
    search_fields = ('title', 'author', 'inventory_number')
    list_filter = ('section', 'address')  # Здесь всё остаётся, Django сам сделает красивый фильтр-выпадашку справа