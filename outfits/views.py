from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Sum, F
from outfits.models import Outfit
from wardrobe.models import Category


from django.shortcuts import render
from django.db.models import Count
from outfits.models import Outfit


from django.shortcuts import render
from django.db.models import Count
from outfits.models import Outfit


def outfit_list(request):
    """Список образов с подсчетом количества вещей через ORM."""
    # ORM-выражение 6: annotate для подсчета + prefetch_related чтобы избежать N+1 запросов
    outfits = Outfit.objects.select_related('user').prefetch_related('items__category').annotate(
        items_count=Count('items')
    ).order_by('name')

    # Примечание: свойство total_cost работает без дополнительных запросов к БД
    # благодаря prefetch_related('items__category')
    return render(request, "outfits/outfit_list.html", {"outfits": outfits})


def outfit_detail(request, outfit_id):
    """Детальная страница образа."""
    # ORM-выражение 7: get_object_or_404 с prefetch_related для связанных вещей
    outfit = get_object_or_404(
        Outfit.objects.prefetch_related('items__category'),
        pk=outfit_id
    )

    return render(request, "outfits/outfit_detail.html", {
        "outfit": outfit,
    })
    # Примечание: total_cost и is_complete доступны как outfit.total_cost и outfit.is_complete
    # благодаря @property в модели, а prefetch_related гарантирует, что это не вызовет новых запросов.


from django.db.models import Count, Sum, F, ExpressionWrapper, DecimalField

from django.shortcuts import render
from django.db.models import Count, Sum, F, ExpressionWrapper, DecimalField
from wardrobe.models import Category


def statistics(request):
    stats = Category.objects.annotate(
        items_count=Count('items'),
        total_cost=Sum(
            ExpressionWrapper(
                F('items__price') * F('items__quantity'),
                output_field=DecimalField()
            ),
            default=0
        )
    ).order_by('-items_count').values('name', 'items_count', 'total_cost')  # <-- Добавили values()

    return render(request, "outfits/statistics.html", {"stats": stats})
