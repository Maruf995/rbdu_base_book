from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Импортируем только нужные модели
from .models import Book, Section

def reader_home(request):
    """Главная страница читателя: красивый поиск и плитка категорий"""
    sections = Section.objects.annotate(total=Count('book')).filter(total__gt=0)
    return render(request, 'catalog/reader_home.html', {'sections': sections})

def book_list(request):
    """Список книг с фильтрацией и пагинацией для читателей"""
    books = Book.objects.all()
    sections = Section.objects.all()
    
    # Получаем уникальные года издания
    years = Book.objects.exclude(publication_year__isnull=True).values_list('publication_year', flat=True).distinct().order_by('-publication_year')

    # Получаем параметры фильтрации
    query = request.GET.get('q') 
    section_id = request.GET.get('section')
    inv_num = request.GET.get('inv_num') 
    year = request.GET.get('year') 
    sort_by = request.GET.get('sort_by') 

    # Применение фильтров
    if query:
        books = books.filter(Q(title__icontains=query) | Q(author__icontains=query))
    if section_id:
        books = books.filter(section_id=section_id)
    if inv_num:
        books = books.filter(inventory_number__icontains=inv_num)
    if year: 
        books = books.filter(publication_year=year)
        
    # Сортировка
    if sort_by == 'author':
        books = books.order_by('author')
    elif sort_by == 'title':
        books = books.order_by('title')
    elif sort_by == 'year_asc':
        books = books.order_by('publication_year') 
    else:
        books = books.order_by('-publication_year', 'title')

    # --- НАЧАЛО БЛОКА ПАГИНАЦИИ ---
    paginator = Paginator(books, 20) # По 20 книг на страницу
    page_number = request.GET.get('page')
    
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1) # Если 'page' не число, даем первую страницу
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages) # Если страница за пределами — последнюю

    # Сохраняем GET-параметры фильтров для ссылок пагинации
    get_params = request.GET.copy()
    if 'page' in get_params:
        del get_params['page']
    url_params = get_params.urlencode() 
    # --- КОНЕЦ БЛОКА ПАГИНАЦИИ ---

    total_books = Book.objects.count()
    categories_stats = Section.objects.annotate(total=Count('book')).filter(total__gt=0)

    context = {
        'books': page_obj,          
        'sections': sections,
        'years': years,
        'total_books': total_books,      
        'categories_stats': categories_stats, 
        'url_params': url_params,   
    }
    return render(request, 'catalog/book_list.html', context)

def book_detail(request, pk):  
    """Детальный просмотр информации о книге"""
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'catalog/book_detail.html', {'book': book})