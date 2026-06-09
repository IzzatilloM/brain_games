"""O'yin ko'rinishlari: kategoriya hub, guruh, to'liq ekran pleyer va natija API."""

import json

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from . import catalog
from .models import Achievement, Game, GameSession, UserAchievement


# --- Yordamchilar -------------------------------------------------------------
def _ensure_game(g):
    """Katalogdagi o'yin uchun Game qatori mavjudligini ta'minlaydi."""
    obj, _ = Game.objects.get_or_create(
        slug=g["slug"],
        defaults={
            "title": g["name"],
            "category": g["category"],
            "kind": g.get("kind", "quiz"),
            "icon": g.get("icon", "🎮"),
            "color": g.get("color", "#7c5cff"),
            "tagline": g.get("tagline", ""),
        },
    )
    return obj


def _parental(user):
    return getattr(user, "parental", None)


def _access(user, category_slug):
    """Ota-ona nazoratiga ko'ra ruxsat holatini qaytaradi."""
    pc = _parental(user)
    if not pc or not pc.is_enabled:
        return {"allowed": True, "reason": ""}
    if pc.is_blocked:
        return {"allowed": False, "reason": "Hisob ota-ona tomonidan vaqtincha bloklangan."}
    if pc.is_within_bedtime():
        return {"allowed": False, "reason": "Tunlik dam olish vaqti. Ertaga davom etamiz! 🌙"}
    if category_slug and not pc.is_category_allowed(category_slug):
        return {"allowed": False, "reason": "Bu kategoriya ota-ona tomonidan o'chirilgan."}
    return {"allowed": True, "reason": ""}


# --- Ko'rinishlar -------------------------------------------------------------
@login_required
def game_hub(request):
    lang = request.session.get("lang", "uz")
    pc = _parental(request.user)
    cats = []
    for cat in catalog.categories_loc(lang):
        allowed = True
        if pc and pc.is_enabled:
            allowed = pc.is_category_allowed(cat["slug"]) and not pc.is_blocked
        cats.append({**cat, "allowed": allowed})
    return render(request, "games/list.html", {"categories": cats})


@login_required
def group_view(request, slug):
    lang = request.session.get("lang", "uz")
    cat = catalog.get_category(slug)
    if not cat:
        return redirect("games:list")
    cat = dict(cat)
    cat["name"] = catalog.loc_name(slug, cat["name"], lang)
    return render(request, "games/group.html", {"category": cat})


@login_required
def subjects_hub(request):
    lang = request.session.get("lang", "uz")
    return render(request, "games/subjects.html", {"subjects": catalog.subjects_loc(lang)})


@login_required
def subject_group(request, slug):
    lang = request.session.get("lang", "uz")
    sub = catalog.get_subject(slug)
    if not sub:
        return redirect("games:subjects")
    sub = dict(sub)
    sub["name"] = catalog.loc_name(slug, sub["name"], lang)
    games = [{"slug": f"{sub['slug']}-{i}", "name": m, "icon": sub["icon"]}
             for i, m in enumerate(sub["modes"], start=1)]
    return render(request, "games/subject_group.html", {"subject": sub, "games": games})


@login_required
def play(request, slug):
    g = catalog.get_game(slug)
    if not g:
        return redirect("games:list")
    access = _access(request.user, g["category"])
    is_subject = g["category"].startswith("fan-")
    if is_subject:
        home_url = f"/oyinlar/fanlar/{g['category']}/"
    else:
        home_url = f"/oyinlar/guruh/{g['category']}/"
    siblings = catalog.siblings_of(slug)
    return render(request, "games/play.html", {
        "game": g,
        "game_json": json.dumps(g, ensure_ascii=False),
        "siblings_json": json.dumps(siblings, ensure_ascii=False),
        "home_url": home_url,
        "access": access,
    })


def _award_achievements(user):
    earned = []
    owned = set(user.achievements.values_list("achievement__code", flat=True))

    def grant(code):
        if code in owned:
            return
        ach = Achievement.objects.filter(code=code).first()
        if not ach:
            return
        UserAchievement.objects.create(user=user, achievement=ach)
        user.coins += ach.coins
        owned.add(code)
        earned.append({"icon": ach.icon, "title": ach.title, "coins": ach.coins})

    total = user.sessions.count()
    if total >= 1:
        grant("first_game")
    if total >= 10:
        grant("ten_games")
    if user.streak_days >= 3:
        grant("streak_3")
    if user.streak_days >= 7:
        grant("streak_7")
    if user.stars >= 25:
        grant("stars_25")
    if user.level >= 5:
        grant("level_5")
    if earned:
        user.save(update_fields=["coins"])
    return earned


@login_required
@require_POST
def submit_session(request, slug):
    g = catalog.get_game(slug)
    if not g:
        return JsonResponse({"ok": False, "reason": "O'yin topilmadi."}, status=404)

    access = _access(request.user, g["category"])
    if not access["allowed"]:
        return JsonResponse({"ok": False, "reason": access["reason"]}, status=403)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        payload = {}

    score = max(0, int(payload.get("score", 0) or 0))
    duration = max(0, int(payload.get("duration", 0) or 0))
    difficulty = max(1, min(3, int(payload.get("difficulty", 1) or 1)))

    xp = max(5, score)
    coins = max(1, score // 5)
    stars = 1 if score >= 50 else 0

    user = request.user
    user.add_rewards(xp=xp, coins=coins, stars=stars)

    game = _ensure_game(g)
    GameSession.objects.create(
        user=user, game=game, score=score,
        xp_earned=xp, coins_earned=coins, stars_earned=stars,
        duration_seconds=duration,
        difficulty_start=difficulty, difficulty_end=difficulty,
    )

    new_achievements = _award_achievements(user)

    return JsonResponse({
        "ok": True,
        "score": score,
        "xp_earned": xp,
        "coins_earned": coins,
        "stars_earned": stars,
        "achievements": new_achievements,
        "profile": {
            "xp": user.xp, "coins": user.coins, "stars": user.stars,
            "streak": user.streak_days, "level": user.level,
            "xp_in_level": user.xp_in_level, "xp_to_next": user.xp_to_next,
        },
    })
