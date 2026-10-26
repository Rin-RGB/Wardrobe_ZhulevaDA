from django.http import HttpResponseNotFound
from django.shortcuts import render

from outfits.models import Outfit


def index(request):
    """Главная страница."""
    recent_outfits = (
        Outfit.objects.select_related("user").prefetch_related("items").all()[:6]
    )
    return render(request, "homepage/index.html", {"recent_outfits": recent_outfits})


def page_not_found(request, exception):
    """Обработчик ошибки 404."""
    return HttpResponseNotFound(
        render(request, "homepage/404.html", status=404),
    )
