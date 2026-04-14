from django.contrib import admin

from .models import Item, ResolutionRequest


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "category", "owner", "date_reported", "is_resolved")
    list_filter = ("status", "category", "is_resolved")
    search_fields = ("title", "description", "location", "owner__username")
    readonly_fields = ("email", "phone")


@admin.register(ResolutionRequest)
class ResolutionRequestAdmin(admin.ModelAdmin):
    list_display = ("item", "requester", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("item__title", "requester__username", "reason")
    readonly_fields = ("created_at", "updated_at")
