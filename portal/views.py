from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ItemForm, UserRegistrationForm, ResolutionRequestForm
from .models import Item, ResolutionRequest


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
    queryset = Item.objects.select_related("owner").filter(is_resolved=False)
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
    user_request = None
    if request.user.is_authenticated:
        user_request = ResolutionRequest.objects.filter(item=item, requester=request.user).first()
    
    context = {
        "item": item,
        "user_request": user_request,
    }
    return render(request, "portal/item_detail.html", context)


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
def request_resolution(request, pk):
    """Owners can request to mark their own item as resolved"""
    item = get_object_or_404(Item, pk=pk)

    if request.user != item.owner:
        messages.error(request, "You can only request resolution for items you posted.")
        return redirect("item_detail", pk=item.pk)

    if item.is_resolved:
        messages.error(request, "This item is already marked as resolved.")
        return redirect("item_detail", pk=item.pk)

    existing_request = ResolutionRequest.objects.filter(item=item, requester=request.user).first()
    if existing_request:
        messages.error(request, "You have already sent a request for this item.")
        return redirect("item_detail", pk=item.pk)

    if request.method == "POST":
        form = ResolutionRequestForm(request.POST)
        if form.is_valid():
            res_request = form.save(commit=False)
            res_request.item = item
            res_request.requester = request.user
            res_request.save()
            messages.success(request, "Resolution request sent to admin for review.")
            return redirect("item_detail", pk=item.pk)
    else:
        form = ResolutionRequestForm()

    return render(request, "portal/request_resolution.html", {"form": form, "item": item})


def is_admin(user):
    """Check if user is admin"""
    return user.is_staff or user.is_superuser


@login_required
@user_passes_test(is_admin, redirect_field_name=None)
def pending_resolutions(request):
    """Admin view for pending resolution requests"""
    requests = ResolutionRequest.objects.filter(
        status=ResolutionRequest.Status.PENDING
    ).select_related("item", "item__owner", "requester")
    
    context = {
        "requests": requests,
        "pending_count": requests.count(),
        "approved_count": ResolutionRequest.objects.filter(status=ResolutionRequest.Status.APPROVED).count(),
        "rejected_count": ResolutionRequest.objects.filter(status=ResolutionRequest.Status.REJECTED).count(),
    }
    return render(request, "portal/pending_resolutions.html", context)


@login_required
@user_passes_test(is_admin, redirect_field_name=None)
def update_resolution_request(request, pk):
    """Admin updates a resolution request using confirm/deny dropdown."""
    res_request = get_object_or_404(ResolutionRequest, pk=pk)

    if request.method != "POST":
        return redirect("pending_resolutions")

    action = request.POST.get("action")
    admin_notes = request.POST.get("admin_notes", "").strip()

    if action == "approve":
        res_request.status = ResolutionRequest.Status.APPROVED
        res_request.admin_notes = admin_notes
        res_request.save()
        res_request.item.is_resolved = True
        res_request.item.save(update_fields=["is_resolved", "updated_at"])
        messages.success(request, f"Resolution approved for '{res_request.item.title}'.")
    elif action == "deny":
        if not admin_notes:
            messages.error(request, "Please provide reason for denial.")
            return redirect("pending_resolutions")
        res_request.status = ResolutionRequest.Status.REJECTED
        res_request.admin_notes = admin_notes
        res_request.save()
        messages.success(request, f"Resolution request denied for '{res_request.item.title}'.")
    else:
        messages.error(request, "Please choose Confirm or Deny before submitting.")

    return redirect("pending_resolutions")


@login_required
@user_passes_test(is_admin, redirect_field_name=None)
def approve_resolution(request, pk):
    """Admin approves a resolution request"""
    res_request = get_object_or_404(ResolutionRequest, pk=pk)
    
    if request.method == "POST":
        admin_notes = request.POST.get("admin_notes", "").strip()
        
        res_request.status = ResolutionRequest.Status.APPROVED
        res_request.admin_notes = admin_notes
        res_request.save()
        
        # Mark the item as resolved
        res_request.item.is_resolved = True
        res_request.item.save(update_fields=["is_resolved", "updated_at"])
        
        messages.success(request, f"Resolution approved for '{res_request.item.title}'.")
        return redirect("pending_resolutions")
    
    return render(request, "portal/approve_resolution.html", {"request_obj": res_request})


@login_required
@user_passes_test(is_admin, redirect_field_name=None)
def reject_resolution(request, pk):
    """Admin rejects a resolution request"""
    res_request = get_object_or_404(ResolutionRequest, pk=pk)
    
    if request.method == "POST":
        admin_notes = request.POST.get("admin_notes", "").strip()
        
        if not admin_notes:
            messages.error(request, "Please provide reason for rejection.")
            return render(request, "portal/reject_resolution.html", {"request_obj": res_request})
        
        res_request.status = ResolutionRequest.Status.REJECTED
        res_request.admin_notes = admin_notes
        res_request.save()
        
        messages.success(request, f"Resolution request rejected for '{res_request.item.title}'.")
        return redirect("pending_resolutions")
    
    return render(request, "portal/reject_resolution.html", {"request_obj": res_request})
