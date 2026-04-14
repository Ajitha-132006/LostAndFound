from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (
    UserLoginView, dashboard, home, item_create, item_detail, item_list,
    my_items, register_view, request_resolution, pending_resolutions,
    update_resolution_request, approve_resolution, reject_resolution
)

urlpatterns = [
    path("", home, name="home"),
    path("dashboard/", dashboard, name="dashboard"),
    path("items/", item_list, name="item_list"),
    path("items/new/", item_create, name="item_create"),
    path("items/<int:pk>/", item_detail, name="item_detail"),
    path("items/<int:pk>/request-resolution/", request_resolution, name="request_resolution"),
    path("my-items/", my_items, name="my_items"),
    path("resolution-requests/", pending_resolutions, name="pending_resolutions"),
    path("resolution-requests/<int:pk>/update/", update_resolution_request, name="update_resolution_request"),
    path("resolution-requests/<int:pk>/approve/", approve_resolution, name="approve_resolution"),
    path("resolution-requests/<int:pk>/reject/", reject_resolution, name="reject_resolution"),
    path("register/", register_view, name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
