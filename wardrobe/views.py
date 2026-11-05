from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from wardrobe.models import ClothingItem, Category
from accounts.models import WardrobeUser

from django.core.paginator import Paginator

from django.shortcuts import render
from django.core.paginator import Paginator
from wardrobe.models import ClothingItem


def clothing_list(request):
    # Базовый запрос + select_related (пункт 19)
    items = ClothingItem.objects.select_related('category', 'user')

    # Пункт 27: exclude() - исключаем вещи, которых нет в наличии
    items = items.exclude(quantity=0)

    # Пункт 13: Динамическая сортировка по параметру запроса
    sort = request.GET.get('sort', 'name')
    sort_fields = {
        'name': 'name',
        'price': 'price',
        '-price': '-price',
        'newest': '-created_at',
    }
    # Защита от произвольного ввода (требование методички)
    order_by_field = sort_fields.get(sort, 'name')
    items = items.order_by(order_by_field)

    # Пункт 22, 23: Пагинация
    paginator = Paginator(items, 6)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, "wardrobe/clothing_list.html", {
        "page_obj": page_obj,
        "items": page_obj,
        "sort": sort,  # Передаем в шаблон, чтобы подсветить активную сортировку
    })

def clothing_detail(request, item_id):
    """Детальная страница вещи."""
    # ORM-выражение 2: Получение одного объекта с обработкой 404 + select_related
    item = get_object_or_404(
        ClothingItem.objects.select_related('category', 'user'),
        pk=item_id
    )
    return render(request, "wardrobe/clothing_detail.html", {"item": item})


def available_items(request):
    """Поиск вещей по сезону и стилю с фильтрацией."""
    season = request.GET.get("season")
    style = request.GET.get("style")

    # ORM-выражение 3: Базовый QuerySet
    queryset = ClothingItem.objects.select_related('category').order_by('price')

    # ORM-выражение 4: Фильтрация по одному условию
    if season:
        queryset = queryset.filter(season=season)

    # ORM-выражение 5: Фильтрация по нескольким условиям (цепочка filter)
    if style:
        queryset = queryset.filter(style=style)

    return render(request, "wardrobe/available.html", {
        "items": queryset,
        "season": season,
        "style": style,
    })