from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('homepage.urls')),
    path('users/', include('accounts.urls')),
    path('clothing/', include('wardrobe.urls')),
    path('outfits/', include('outfits.urls')),
]

handler404 = 'homepage.views.page_not_found'
