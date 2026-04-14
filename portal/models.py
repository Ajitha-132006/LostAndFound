from django.conf import settings
from django.db import models
from django.utils import timezone


class Item(models.Model):
    class Category(models.TextChoices):
        ELECTRONICS = "electronics", "Electronics"
        DOCUMENTS = "documents", "Documents"
        ACCESSORIES = "accessories", "Accessories"
        STATIONERY = "stationery", "Stationery"
        OTHERS = "others", "Others"

    class Status(models.TextChoices):
        LOST = "lost", "Lost"
        FOUND = "found", "Found"

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="items")
    title = models.CharField(max_length=120)
    category = models.CharField(max_length=30, choices=Category.choices, default=Category.OTHERS)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.LOST)
    description = models.TextField()
    location = models.CharField(max_length=160)
    date_reported = models.DateField(default=timezone.now)
    image = models.ImageField(upload_to="items/", blank=True, null=True)
    is_resolved = models.BooleanField(default=False)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["category"]),
            models.Index(fields=["is_resolved"]),
        ]

    def __str__(self) -> str:
        return f"{self.title} ({self.get_status_display()})"


class ResolutionRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="resolution_requests")
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_resolution_requests")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    reason = models.TextField(help_text="Why do you think this item should be marked as resolved?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_notes = models.TextField(blank=True, help_text="Admin notes on this request")

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["item", "requester"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["item"]),
        ]

    def __str__(self) -> str:
        return f"Resolution request for {self.item.title} by {self.requester.username}"
