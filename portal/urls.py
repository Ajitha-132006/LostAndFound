from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import UserLoginView, dashboard, home, item_create, item_detail, item_list, mark_resolved, my_items, register_view

urlpatterns = [
    path("", home, name="home"),
    path("dashboard/", dashboard, name="dashboard"),
    path("items/", item_list, name="item_list"),
    path("items/new/", item_create, name="item_create"),
    path("items/<int:pk>/", item_detail, name="item_detail"),
    path("items/<int:pk>/resolve/", mark_resolved, name="mark_resolved"),
    path("my-items/", my_items, name="my_items"),
    path("register/", register_view, name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
