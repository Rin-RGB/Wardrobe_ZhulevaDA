from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Sum, F
from accounts.models import WardrobeUser


def user_list(request):
    """Список пользователей с агрегацией данных через ORM."""
    # Добавляем аннотации для подсчета вещей и стоимости
    users = WardrobeUser.objects.annotate(
        items_count=Count('clothing_items'),
        total_cost=Sum(F('clothing_items__price') * F('clothing_items__quantity'), default=0)
    ).order_by('name')

    return render(request, "accounts/user_list.html", {"users": users})


def user_detail(request, user_id):
    """Профиль пользователя с его вещами."""
    user = get_object_or_404(
        WardrobeUser.objects.annotate(
            items_count=Count('clothing_items'),
            total_cost=Sum(F('clothing_items__price') * F('clothing_items__quantity'), default=0)
        ),
        pk=user_id
    )

    clothing_items = user.clothing_items.select_related('category').order_by('name')

    return render(
        request,
        "accounts/user_detail.html",
        {
            "user": user,
            "clothing_items": clothing_items,
        }
    )