from django.db import models

# 1. Создаем новую модель для Отраслей знания
class Section(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Название раздела")

    class Meta:
        verbose_name = "Раздел (Отрасль знания)"
        verbose_name_plural = "Разделы (Отрасли знания)"
        ordering = ['name']

    def __str__(self):
        return self.name

class Book(models.Model):
    address = models.CharField(max_length=150, verbose_name="Адрес", default="Хранение")
    
    # 2. МЕНЯЕМ поле section на связь ForeignKey (выпадающий список)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Разделы (Отрасль знания)")
    
    author = models.CharField(max_length=200, blank=True, null=True, verbose_name="Фамилия автора")
    title = models.CharField(max_length=300, verbose_name="Название книги")
    inventory_number = models.CharField(max_length=50, unique=True, verbose_name="Инвентариз. №")
    cipher = models.CharField(max_length=100, blank=True, null=True, verbose_name="Шифр")
    publication_year = models.IntegerField(blank=True, null=True, verbose_name="Год выпуска")
    note = models.TextField(blank=True, null=True, verbose_name="Примечание")
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Стоимость книг")

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ['title']

    def __str__(self):
        return f"{self.title} - {self.author or 'Без автора'}"