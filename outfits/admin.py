from django.contrib import admin

from .models import Outfit


@admin.register(Outfit)
class OutfitAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "occasion", "season", "created_at")
    list_filter = ("user", "occasion", "season")
    filter_horizontal = ("items",)
