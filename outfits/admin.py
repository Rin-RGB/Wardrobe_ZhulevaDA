from django.contrib import admin
from .models import Outfit


@admin.register(Outfit)
class OutfitAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "occasion", "season", "created_at", "is_complete")
    list_filter = ("user", "occasion", "season")
    search_fields = ("name", "user__name")
    filter_horizontal = ("items",)       # Критерий 2 (удобная работа со связанными M2M объектами)
    ordering = ("-created_at",)
    list_per_page = 20
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("total_cost", "created_at")