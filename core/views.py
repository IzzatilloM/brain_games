"""Asosiy sahifalar: home, statistika, reyting, yordam, multipleyer, uy vazifalari."""

import json
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Sum
from django.shortcuts import redirect, render
from django.utils import timezone

from games.catalog import CATEGORIES, categories_loc
from games.models import GameSession

User = get_user_model()


@login_required
def home(request):
    lang = request.session.get("lang", "uz")
    total_games = sum(len(c["games"]) for c in CATEGORIES)
    return render(request, "core/home.html", {
        "categories": categories_loc(lang),
        "total_games": total_games,
    })


def about(request):
    return render(request, "core/about.html")


def set_lang(request, code):
    from games.catalog import CATEGORIES  # noqa
    from core.translations import LANG_CODES
    if code in LANG_CODES:
        request.session["lang"] = code
    return redirect(request.META.get("HTTP_REFERER") or "core:home")


@login_required
def help_page(request):
    faqs = [
        {"icon": "🎮", "q": "Qanday o'ynayman?", "a": "Chap menyudan «O'yinlar» bo'limiga o'ting, kategoriyani tanlang va o'yinni boshlang."},
        {"icon": "🪙", "q": "Tanga va yulduzlar nima?", "a": "Har bir o'yin uchun XP, tanga va yulduz olasiz. Ular bilan darajangiz oshadi."},
        {"icon": "🏆", "q": "Reyting qanday ishlaydi?", "a": "Reyting XP bo'yicha tuziladi — qancha ko'p o'ynasangiz, shuncha yuqoriga ko'tarilasiz."},
        {"icon": "🔥", "q": "Ketma-ketlik (streak) nima?", "a": "Har kuni kamida bitta o'yin o'ynasangiz, ketma-ketlik kunlari oshib boradi."},
        {"icon": "👨‍👩‍👧", "q": "Ota-ona nazorati nima?", "a": "Ota-ona PIN kod orqali kirib, kunlik vaqt chegarasi va ruxsatlarni sozlashi mumkin."},
        {"icon": "🌙", "q": "Tungi rejim bormi?", "a": "Ha! Navbardagi oy tugmasi orqali yorug'/qorong'i rejimni almashtiring."},
    ]
    return render(request, "core/help.html", {"faqs": faqs})


@login_required
def multiplayer(request):
    return render(request, "core/multiplayer.html")


@login_required
def homework(request):
    return render(request, "core/homework.html")


@login_required
def stats(request):
    user = request.user
    games = GameSession.objects.filter(user=user)

    today = timezone.localdate()
    labels_uz = ["Du", "Se", "Ch", "Pa", "Ju", "Sh", "Ya"]
    weekly = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        xp = games.filter(created_at__date=day).aggregate(s=Sum("xp_earned"))["s"] or 0
        weekly.append({"label": labels_uz[day.weekday()], "xp": xp})

    totals = {
        "games": games.count(),
        "best": games.aggregate(m=Max("score"))["m"] or 0,
        "xp": user.xp,
        "minutes": round((games.aggregate(s=Sum("duration_seconds"))["s"] or 0) / 60),
    }
    return render(request, "core/stats.html", {
        "weekly_json": json.dumps(weekly, ensure_ascii=False),
        "totals": totals,
    })


@login_required
def rating(request):
    top = User.objects.order_by("-xp", "-stars")[:60]
    rows = []
    for i, u in enumerate(top, start=1):
        rows.append({
            "rank": i,
            "name": u.display_name,
            "avatar": u.avatar,
            "city": u.city or "Toshkent",
            "xp": u.xp,
            "level": u.level,
            "stars": u.stars,
            "is_me": u.id == request.user.id,
        })
    my_rank = User.objects.filter(xp__gt=request.user.xp).count() + 1
    total = User.objects.count()
    lang = request.session.get("lang", "uz") if hasattr(request, "session") else "uz"
    months = {
        "uz": ["Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun", "Iyul",
               "Avgust", "Sentyabr", "Oktyabr", "Noyabr", "Dekabr"],
        "ru": ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль",
               "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"],
        "en": ["January", "February", "March", "April", "May", "June", "July",
               "August", "September", "October", "November", "December"],
    }
    now = timezone.localtime()
    cur_month = "%s %s" % (months.get(lang, months["uz"])[now.month - 1], now.year)
    return render(request, "core/rating.html", {
        "rows": rows, "my_rank": my_rank, "total": total, "cur_month": cur_month,
    })
