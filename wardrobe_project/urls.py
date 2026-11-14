from django.contrib import admin
from django.urls import path, include
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),  # <-- ДОБАВЬ ЭТУ СТРОКУ
    path('', include('homepage.urls', namespace='homepage')),
    path('clothing/', include('wardrobe.urls', namespace='wardrobe')),
    path('outfits/', include('outfits.urls', namespace='outfits')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
]

handler404 = "homepage.views.page_not_found"
