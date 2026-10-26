from django.urls import path

from . import views

app_name = "wardrobe"

urlpatterns = [
    path("", views.clothing_list, name="clothing_list"),
    path("<int:item_id>/", views.clothing_detail, name="clothing_detail"),
    path("available/", views.available_items, name="available_items"),
]
