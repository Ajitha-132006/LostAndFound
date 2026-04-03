from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Item


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["title", "category", "status", "description", "location", "date_reported", "image"]
        widgets = {
            "date_reported": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 4}),
        }
