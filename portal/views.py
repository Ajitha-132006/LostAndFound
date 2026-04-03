from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ItemForm, UserRegistrationForm
from .models import Item


def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "portal/landing.html")


@login_required
def dashboard(request):
    context = {
        "total_items": Item.objects.count(),
        "lost_items": Item.objects.filter(status=Item.Status.LOST, is_resolved=False).count(),
        "found_items": Item.objects.filter(status=Item.Status.FOUND, is_resolved=False).count(),
        "recent_items": Item.objects.select_related("owner")[:5],
    }
    return render(request, "portal/dashboard.html", context)


def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect("dashboard")
    else:
        form = UserRegistrationForm()
    return render(request, "registration/register.html", {"form": form})


class UserLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = AuthenticationForm


def item_list(request):
    queryset = Item.objects.select_related("owner").all()
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()
    category = request.GET.get("category", "").strip()

    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(location__icontains=query)
        )

    if status in {Item.Status.LOST, Item.Status.FOUND}:
        queryset = queryset.filter(status=status)

    if category in dict(Item.Category.choices):
        queryset = queryset.filter(category=category)

    context = {
        "items": queryset,
        "q": query,
        "status": status,
        "category": category,
        "status_choices": Item.Status.choices,
        "category_choices": Item.Category.choices,
    }
    return render(request, "portal/item_list.html", context)


def item_detail(request, pk):
    item = get_object_or_404(Item.objects.select_related("owner"), pk=pk)
    return render(request, "portal/item_detail.html", {"item": item})


@login_required
def item_create(request):
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            messages.success(request, "Item posted successfully.")
            return redirect("item_detail", pk=item.pk)
    else:
        form = ItemForm()
    return render(request, "portal/item_form.html", {"form": form})


@login_required
def my_items(request):
    items = Item.objects.filter(owner=request.user)
    return render(request, "portal/my_items.html", {"items": items})


@login_required
def mark_resolved(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        if item.owner == request.user or request.user.is_staff:
            item.is_resolved = True
            item.save(update_fields=["is_resolved", "updated_at"])
            messages.success(request, "Item marked as resolved.")
        else:
            messages.error(request, "You do not have permission to update this item.")
    return redirect("item_detail", pk=item.pk)
