"""Autentifikatsiya: kirish, ro'yxat, profil va ota-ona nazorati."""

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import (
    LoginForm,
    ParentalControlForm,
    ParentalUnlockForm,
    ProfileForm,
    RegisterForm,
)
from .models import AGE_GROUPS, AVATARS, ParentalControl


def login_view(request):
    if request.user.is_authenticated:
        return redirect("core:home")
    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        user.touch_activity()
        messages.success(request, f"Xush kelibsiz, {user.display_name}! 🎉")
        return redirect("core:home")
    return render(request, "accounts/login.html", {"form": form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect("core:home")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        user.touch_activity()
        messages.success(request, "Ro'yxatdan o'tdingiz! Sayohatni boshlaymiz 🚀")
        return redirect("core:home")
    return render(request, "accounts/register.html", {
        "form": form,
        "avatars": AVATARS,
        "age_groups": AGE_GROUPS,
    })


@login_required
def logout_view(request):
    request.session.pop("parental_unlocked", None)
    logout(request)
    messages.info(request, "Hisobingizdan chiqdingiz. Yana kutamiz! 👋")
    return redirect("accounts:login")


@login_required
def profile_view(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profil yangilandi ✅")
        return redirect("accounts:profile")
    return render(request, "accounts/profile.html", {
        "form": form,
        "avatars": AVATARS,
    })


# --- Ota-ona nazorati ---------------------------------------------------------
def _send_parental_email(pc):
    """Ota-ona nazorati yoqilganini emailga (Gmail) yuboradi."""
    if not pc.parent_email:
        return
    who = "Otasi" if pc.parent_type == "ota" else "Onasi"
    body = (
        f"Assalomu alaykum, {pc.parent_first_name} {pc.parent_last_name}!\n\n"
        f"BrainGames platformasida ota-ona nazorati MUVAFFAQIYATLI YOQILDI ✅\n\n"
        f"Ota-ona: {who} — {pc.parent_first_name} {pc.parent_last_name}\n"
        f"Farzand: {pc.child_first_name} {pc.child_last_name}\n"
        f"Kunlik vaqt chegarasi: {pc.daily_limit_minutes} daqiqa\n\n"
        f"Endi farzandingiz faolligini nazorat qilishingiz mumkin.\n— BrainGames jamoasi"
    )
    try:
        from django.conf import settings as dj
        from django.core.mail import send_mail
        send_mail(
            "BrainGames — Ota-ona nazorati yoqildi",
            body,
            getattr(dj, "DEFAULT_FROM_EMAIL", "noreply@braingames.uz"),
            [pc.parent_email],
            fail_silently=True,
        )
    except Exception:
        pass


@login_required
def parental_view(request):
    from .forms import ParentRegisterForm
    pc, _ = ParentalControl.objects.get_or_create(user=request.user)

    # 1) Hali ro'yxatdan o'tmagan — ota-ona ro'yxati
    if not pc.registered:
        form = ParentRegisterForm(request.POST or None, instance=pc)
        if request.method == "POST" and form.is_valid():
            obj = form.save(commit=False)
            obj.registered = True
            obj.is_enabled = True
            obj.save()
            _send_parental_email(obj)
            request.session["parental_just"] = True
            messages.success(request, "Ota-ona nazorati muvaffaqiyatli yoqildi ✅")
            return redirect("accounts:parental")
        return render(request, "accounts/parental_register.html", {"form": form, "pc": pc})

    # 2) Ro'yxatdan o'tgan — sozlamalar + modal
    show_modal = request.session.pop("parental_just", False)
    form = ParentalControlForm(instance=pc)
    return render(request, "accounts/parental.html", {
        "form": form, "pc": pc, "show_modal": show_modal,
    })


@login_required
def parental_save(request):
    pc, _ = ParentalControl.objects.get_or_create(user=request.user)
    if not request.session.get("parental_unlocked"):
        return redirect("accounts:parental")
    form = ParentalControlForm(request.POST, instance=pc)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.is_enabled = True
        obj.save()
        messages.success(request, "Ota-ona nazorati saqlandi ✅")
    else:
        messages.error(request, "Sozlamalarni saqlashda xatolik.")
    return redirect("accounts:parental")
