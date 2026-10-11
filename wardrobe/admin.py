from django.contrib import admin
from .models import Category, ClothingItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(ClothingItem)
class ClothingItemAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'user', 'category', 'color', 'season', 'price', 'quantity',
    )
    list_filter = ('user', 'category', 'season', 'style')
    search_fields = ('name', 'color')
