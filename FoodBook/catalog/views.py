from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import FoodEntryForm
from .models import FoodEntry



def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def add_entry(request):
    if request.method == "POST":
        form = FoodEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.owner = request.user
            entry.save()
            return redirect("home")
    else:
        form = FoodEntryForm()
    return render(request, "catalog/add.html", {"form": form})


def home(request):
    query = request.GET.get("q", "").strip()
    if query:
        _require_local_debug(request)
    entries = FoodEntry.objects.all().order_by("-created_at")
    if query:
        entries = entries.filter(name__icontains=query)
    return render(request, "catalog/home.html", {"entries": entries, "query": query})


@staff_member_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(FoodEntry, pk=entry_id)
    if request.method == "POST":
        form = FoodEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = FoodEntryForm(instance=entry)
    return render(request, "catalog/edit.html", {"form": form, "entry": entry})


@staff_member_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(FoodEntry, pk=entry_id)
    if request.method == "POST":
        entry.delete()
        return redirect("home")
    return render(request, "catalog/delete.html", {"entry": entry})


def _require_local_debug(request):
    # Учебные IDOR-маршруты не должны работать вне локальной DEBUG-среды.
    if not settings.DEBUG or request.META.get("REMOTE_ADDR") not in {"127.0.0.1", "::1"}:
        raise Http404


@login_required
def idor_insecure_demo(request, entry_id):
    _require_local_debug(request)
    # Намеренно небезопасно для учебного сравнения: владелец не проверяется.
    entry = get_object_or_404(FoodEntry, pk=entry_id)
    return render(request, "catalog/lab_record.html", {"entry": entry, "mode": "insecure"})


