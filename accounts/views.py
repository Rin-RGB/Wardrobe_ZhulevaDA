from django.shortcuts import get_object_or_404, render

from .models import WardrobeUser


def user_list(request):
    """Список всех пользователей."""
    users = WardrobeUser.objects.all()
    return render(request, 'accounts/user_list.html', {'users': users})


def user_detail(request, user_id):
    """Страница пользователя с его гардеробом."""
    user = get_object_or_404(WardrobeUser, pk=user_id)
    clothing_items = user.clothing_items.select_related('category').all()
    outfits = user.outfits.all()
    context = {
        'user': user,
        'clothing_items': clothing_items,
        'outfits': outfits,
        'total_cost': user.get_wardrobe_cost(),
        'total_items': user.get_items_count(),
    }
    return render(request, 'accounts/user_detail.html', context)
