from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Item


class ItemModelTests(TestCase):
    def test_item_string_representation(self):
        user = User.objects.create_user(username="alice", password="password123")
        item = Item.objects.create(
            owner=user,
            title="ID Card",
            category=Item.Category.DOCUMENTS,
            status=Item.Status.LOST,
            description="Lost near library",
            location="Library",
        )
        self.assertIn("ID Card", str(item))


class ItemViewTests(TestCase):
    def test_item_list_page_loads(self):
        response = self.client.get(reverse("item_list"))
        self.assertEqual(response.status_code, 200)
