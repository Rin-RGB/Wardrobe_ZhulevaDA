from django.core.paginator import Paginator
from django.db import models
from django.db.models import Avg, Count, F, Q, Sum
from django.shortcuts import get_object_or_404, render

from wardrobe.models import ClothingItem, SeasonChoices, StyleChoices


def clothing_list(request):
    # 1. Базовый запрос + select_related + exclude
    items = ClothingItem.objects.select_related('category', 'user').exclude(quantity=0)

    # 2. ПОИСК (закрывает пункты 7 и 8 методички)
    search_query = request.GET.get('q', '').strip()
    if search_query:
        items = items.filter(
            Q(name__icontains=search_query) | Q(color__icontains=search_query)
        )

    # 3. Динамическая сортировка (Критерий 11)
    sort = request.GET.get('sort', 'name')
    sort_fields = {
        'name': 'name',
        'price': 'price',
        '-price': '-price',
        'newest': '-created_at',
    }

    # Обработка некорректных значений (Критерий 10)
    if sort not in sort_fields:
        sort = 'name'

    items = items.order_by(sort_fields.get(sort, 'name'))

    # 4. Пагинация (Критерий 21)
    paginator = Paginator(items, 6)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, "wardrobe/clothing_list.html", {
        "page_obj": page_obj,
        "items": page_obj,
        "sort": sort,
        "search_query": search_query,
    })


def clothing_detail(request, slug):
    """Детальная страница вещи (Критерии 14, 15, 27)."""
    item = get_object_or_404(
        ClothingItem.objects.select_related('category', 'user'),
        slug=slug,
    )
    return render(request, "wardrobe/clothing_detail.html", {"item": item})


def available_items(request):
    """Поиск вещей по сезону и стилю с фильтрацией."""
    season = request.GET.get("season")
    style = request.GET.get("style")

    queryset = ClothingItem.objects.select_related('category').order_by('price')

    if season:
        queryset = queryset.filter(season=season)

    if style:
        queryset = queryset.filter(style=style)

    return render(request, "wardrobe/available.html", {
        "items": queryset,
        "season": season,
        "style": style,
    })


def statistics(request):
    """Страница со статистикой гардероба (Критерии 17, 18)."""

    # --- Критерий 17: агрегация по всей таблице ---
    total_stats = ClothingItem.objects.aggregate(
        total_items=Count('id'),
        total_quantity=Sum('quantity'),
        total_cost=Sum(
            F('price') * F('quantity'),
            output_field=models.DecimalField(max_digits=12, decimal_places=2),
        ),
        avg_price=Avg('price'),
        winter_count=Count('id', filter=Q(season=SeasonChoices.WINTER)),
        summer_count=Count('id', filter=Q(season=SeasonChoices.SUMMER)),
        expensive_count=Count('id', filter=Q(price__gte=5000)),
    )

    # --- Критерий 18: групповая статистика по категориям ---
    # values() задаёт GROUP BY, annotate() считает агрегаты внутри группы
    category_stats = (
        ClothingItem.objects
        .values('category__name')
        .annotate(
            items_count=Count('id'),
            total_cost=Sum(
                F('price') * F('quantity'),
                output_field=models.DecimalField(max_digits=12, decimal_places=2),
            ),
            avg_price=Avg('price'),
        )
        .order_by('-items_count')
    )

    # --- Групповая статистика по сезонам ---
    # values() возвращает словари, поэтому подписи подставляем здесь,
    # а не в шаблоне (Критерий 12)
    season_labels = dict(SeasonChoices.choices)
    season_stats = [
        {
            'code': row['season'],
            'label': season_labels.get(row['season'], row['season']),
            'items_count': row['items_count'],
        }
        for row in (
            ClothingItem.objects
            .values('season')
            .annotate(items_count=Count('id'))
            .order_by('-items_count')
        )
    ]

    # --- Групповая статистика по стилям ---
    style_labels = dict(StyleChoices.choices)
    style_stats = [
        {
            'code': row['style'],
            'label': style_labels.get(row['style'], row['style']),
            'items_count': row['items_count'],
        }
        for row in (
            ClothingItem.objects
            .values('style')
            .annotate(items_count=Count('id'))
            .order_by('-items_count')
        )
    ]

    context = {
        'total_stats': total_stats,
        'category_stats': category_stats,
        'season_stats': season_stats,
        'style_stats': style_stats,
    }
    return render(request, 'wardrobe/statistics.html', context)