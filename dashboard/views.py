"""Kabinet ko'rinishlari: o'quvchi paneli va ota-ona nazorat paneli."""

from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Sum
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.forms import AddChildForm, ParentalControlForm
from accounts.models import ParentalControl, User
from games.models import Game, GameSession, Progress


def _weekly_activity(user):
    """Oxirgi 7 kun bo'yicha kunlik daqiqalar (chart uchun)."""
    today = timezone.localdate()
    days, labels = [], []
    names = ["Du", "Se", "Ch", "Pa", "Ju", "Sh", "Ya"]
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        seconds = (
            GameSession.objects.filter(user=user, created_at__date=day).aggregate(
                total=Sum("duration_seconds")
            )["total"]
            or 0
        )
        days.append(round(seconds / 60))
        labels.append(names[day.weekday()])
    return labels, days


def _today_minutes(user):
    today = timezone.localdate()
    seconds = (
        GameSession.objects.filter(user=user, created_at__date=today).aggregate(
            total=Sum("duration_seconds")
        )["total"]
        or 0
    )
    return round(seconds / 60)


@login_required
def home(request):
    """Rolga qarab kerakli panelga yo'naltiradi."""
    if request.user.is_parent:
        return parent_dashboard(request)
    return student_dashboard(request)


def student_dashboard(request):
    user = request.user
    progress = (
        Progress.objects.filter(user=user)
        .select_related("game")
        .order_by("-total_sessions")
    )
    sessions = (
        GameSession.objects.filter(user=user).select_related("game")[:8]
    )
    achievements = user.achievements.select_related("achievement")[:8]
    labels, minutes = _weekly_activity(user)

    totals = GameSession.objects.filter(user=user).aggregate(
        total_q=Sum("questions_total"),
        total_c=Sum("questions_correct"),
        plays=Count("id"),
    )
    accuracy = 0
    if totals["total_q"]:
        accuracy = round(totals["total_c"] / totals["total_q"] * 100)

    controls = getattr(user, "controls", None)
    today_minutes = _today_minutes(user)

    context = {
        "progress_list": progress,
        "sessions": sessions,
        "achievements": achievements,
        "chart_labels": labels,
        "chart_minutes": minutes,
        "accuracy": accuracy,
        "plays": totals["plays"] or 0,
        "controls": controls,
        "today_minutes": today_minutes,
        "time_left": (controls.daily_time_limit - today_minutes) if controls else None,
    }
    return render(request, "dashboard/student.html", context)


def parent_dashboard(request):
    parent = request.user
    children = parent.children.all().prefetch_related("controls")
    rows = []
    for child in children:
        labels, minutes = _weekly_activity(child)
        agg = GameSession.objects.filter(user=child).aggregate(
            total_q=Sum("questions_total"),
            total_c=Sum("questions_correct"),
            plays=Count("id"),
        )
        acc = 0
        if agg["total_q"]:
            acc = round(agg["total_c"] / agg["total_q"] * 100)
        rows.append({
            "child": child,
            "today_minutes": _today_minutes(child),
            "week_minutes": sum(minutes),
            "accuracy": acc,
            "plays": agg["plays"] or 0,
            "controls": getattr(child, "controls", None),
        })
    return render(request, "dashboard/parent.html", {"rows": rows})


@login_required
def add_child(request):
    if not request.user.is_parent:
        raise Http404
    form = AddChildForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        child = form.save(parent=request.user)
        messages.success(request, f"{child.full_name} muvaffaqiyatli qo'shildi! 🎉")
        return redirect("dashboard:home")
    return render(request, "dashboard/add_child.html", {"form": form})


@login_required
def child_detail(request, child_id):
    if not request.user.is_parent:
        raise Http404
    child = get_object_or_404(User, id=child_id, parent=request.user)

    control, _ = ParentalControl.objects.get_or_create(child=child)
    form = ParentalControlForm(request.POST or None, instance=control)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Nazorat sozlamalari saqlandi ✅")
        return redirect("dashboard:child_detail", child_id=child.id)

    progress = Progress.objects.filter(user=child).select_related("game")
    sessions = GameSession.objects.filter(user=child).select_related("game")[:15]
    labels, minutes = _weekly_activity(child)
    agg = GameSession.objects.filter(user=child).aggregate(
        total_q=Sum("questions_total"),
        total_c=Sum("questions_correct"),
        avg_diff=Avg("difficulty_end"),
    )
    acc = 0
    if agg["total_q"]:
        acc = round(agg["total_c"] / agg["total_q"] * 100)

    context = {
        "child": child,
        "form": form,
        "progress_list": progress,
        "sessions": sessions,
        "chart_labels": labels,
        "chart_minutes": minutes,
        "accuracy": acc,
        "avg_difficulty": round(agg["avg_diff"] or 0, 1),
        "today_minutes": _today_minutes(child),
    }
    return render(request, "dashboard/child_detail.html", context)
