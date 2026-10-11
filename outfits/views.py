from django.shortcuts import get_object_or_404, render

from .models import Outfit


def outfit_list(request):
    """Список всех образов."""
    outfits = Outfit.objects.select_related('user').prefetch_related('items').all()
    return render(request, 'outfits/outfit_list.html', {'outfits': outfits})


def outfit_detail(request, outfit_id):
    """Страница отдельного образа."""
    outfit = get_object_or_404(
        Outfit.objects.select_related('user').prefetch_related('items'),
        pk=outfit_id,
    )
    return render(request, 'outfits/outfit_detail.html', {'outfit': outfit})
