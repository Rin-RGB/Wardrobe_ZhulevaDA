from django.urls import path
from . import views

app_name = 'outfits'

urlpatterns = [
    path('', views.outfit_list, name='outfit_list'),
    path('<int:outfit_id>/', views.outfit_detail, name='outfit_detail'),
]
