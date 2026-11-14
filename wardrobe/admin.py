from django.contrib import admin
from .models import Category, ClothingItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(ClothingItem)
class ClothingItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
        "category",
        "color",
        "season",
        "style",
        "price",
        "quantity",
    )
    list_filter = ("user", "category", "season", "style")
    search_fields = ("name", "color", "user__name")
    ordering = ("-created_at",)          # Критерий 6
    list_per_page = 20                   # Критерий 6
    prepopulated_fields = {"slug": ("name",)}  # Критерий 15
    readonly_fields = ("total_cost", "created_at")