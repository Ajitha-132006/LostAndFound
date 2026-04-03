from django.contrib import admin

from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "category", "owner", "date_reported", "is_resolved")
    list_filter = ("status", "category", "is_resolved")
    search_fields = ("title", "description", "location", "owner__username")
    list_editable = ("is_resolved",)
