from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Book, Section  # Не забудьте импортировать Section

# Регистрируем Разделы
@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(ImportExportModelAdmin):
    list_display = ('inventory_number', 'title', 'author', 'section', 'publication_year')
    search_fields = ('title', 'author', 'inventory_number')
    list_filter = ('section', 'address')