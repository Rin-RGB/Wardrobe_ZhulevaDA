from django.contrib import admin
from .models import WardrobeUser


@admin.register(WardrobeUser)
class WardrobeUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')
