from django.shortcuts import get_object_or_404, render

from accounts.models import WardrobeUser
from .models import Category, ClothingItem


def clothing_list(request):
    """Список всех вещей в системе."""
    items = ClothingItem.objects.select_related('user', 'category').all()
    categories = Category.objects.all()
    context = {
        'items': items,
        'categories': categories,
        'total_items': sum(item.quantity for item in items),
    }
    return render(request, 'wardrobe/clothing_list.html', context)


def clothing_detail(request, item_id):
    """Страница отдельной вещи."""
    item = get_object_or_404(
        ClothingItem.objects.select_related('user', 'category'),
        pk=item_id,
    )
    return render(request, 'wardrobe/clothing_detail.html', {'item': item})


def user_wardrobe(request, user_id):
    """Гардероб конкретного пользователя."""
    user = get_object_or_404(WardrobeUser, pk=user_id)
    items = user.clothing_items.select_related('category').all()
    context = {
        'user': user,
        'items': items,
        'total_items': sum(item.quantity for item in items),
        'total_cost': user.get_wardrobe_cost(),
    }
    return render(request, 'wardrobe/user_wardrobe.html', context)
