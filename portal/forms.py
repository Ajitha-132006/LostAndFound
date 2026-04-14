from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Item, ResolutionRequest


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["title", "category", "status", "description", "location", "date_reported", "image", "email", "phone"]
        widgets = {
            "date_reported": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 4}),
            "email": forms.EmailInput(attrs={"placeholder": "your-email@example.com"}),
            "phone": forms.TextInput(attrs={"placeholder": "+1234567890", "type": "tel"}),
        }


class ResolutionRequestForm(forms.ModelForm):
    class Meta:
        model = ResolutionRequest
        fields = ["reason"]
        widgets = {
            "reason": forms.Textarea(attrs={"rows": 4, "placeholder": "Explain why this item should be marked as resolved..."}),
        }
