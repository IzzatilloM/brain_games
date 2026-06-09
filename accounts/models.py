"""Foydalanuvchi modeli — bitta bola hisobi (BrainGames / MindSkills uslubi).

Ota-ona/farzand rollari yo'q. Ota-ona nazorati platforma ichidagi alohida
sahifa orqali (PIN bilan) yoqiladi.
"""

from datetime import time

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Yosh guruhlari va avatarlar (ro'yxatdan o'tishda tanlanadi)
AGE_GROUPS = [
    ("6-8", "6-8 yosh"),
    ("9-11", "9-11 yosh"),
    ("12-14", "12-14 yosh"),
]

AVATARS = [
    "🦁", "🐯", "🦊", "🐼", "🐨", "🐵", "🦉", "🐲",
    "🚀", "⭐", "🤖", "🦄", "🐶", "🐱", "🐸", "🐧",
]

XP_PER_LEVEL = 100


class User(AbstractUser):
    """Kengaytirilgan foydalanuvchi: o'quvchi (bola) profili + gamifikatsiya."""

    full_name = models.CharField("To'liq ism", max_length=120, blank=True)
    age_group = models.CharField(
        "Yosh guruhi", max_length=10, choices=AGE_GROUPS, default="9-11"
    )
    avatar = models.CharField("Avatar", max_length=8, default="🦁")
    city = models.CharField("Shahar", max_length=60, blank=True, default="Toshkent")

    # Gamifikatsiya
    xp = models.PositiveIntegerField("Tajriba (XP)", default=0)
    coins = models.PositiveIntegerField("Tangalar", default=15)
    stars = models.PositiveIntegerField("Yulduzlar", default=0)
    streak_days = models.PositiveIntegerField("Ketma-ket kunlar", default=0)
    last_active = models.DateField("Oxirgi faollik", null=True, blank=True)

    # Sozlamalar
    sound_enabled = models.BooleanField("Ovoz yoniq", default=True)
    language = models.CharField("Til", max_length=5, default="uz")

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"

    def __str__(self):
        return self.full_name or self.username

    # --- Ko'rsatkichlar -------------------------------------------------------
    @property
    def display_name(self):
        return self.full_name or self.first_name or self.username

    @property
    def level(self):
        return self.xp // XP_PER_LEVEL + 1

    @property
    def xp_in_level(self):
        """Joriy darajadagi foiz (0-100)."""
        return int(self.xp % XP_PER_LEVEL)

    @property
    def xp_to_next(self):
        return XP_PER_LEVEL - (self.xp % XP_PER_LEVEL)

    # --- Mukofot / faollik ----------------------------------------------------
    def add_rewards(self, xp=0, coins=0, stars=0):
        self.xp += max(0, int(xp))
        self.coins += max(0, int(coins))
        self.stars += max(0, int(stars))
        self.touch_activity(save=False)
        self.save(update_fields=["xp", "coins", "stars", "streak_days", "last_active"])

    def touch_activity(self, save=True):
        today = timezone.localdate()
        if self.last_active == today:
            return
        if self.last_active == today - timezone.timedelta(days=1):
            self.streak_days += 1
        else:
            self.streak_days = 1
        self.last_active = today
        if save:
            self.save(update_fields=["streak_days", "last_active"])


class ParentalControl(models.Model):
    """Platforma ichidagi ota-ona nazorati — PIN bilan yoqiladi."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="parental",
        verbose_name="Foydalanuvchi",
    )
    pin = models.CharField("Ota-ona PIN kodi", max_length=8, default="0000")
    is_enabled = models.BooleanField("Nazorat yoqilgan", default=False)

    # Ota-ona ro'yxati
    PARENT_TYPES = [("ota", "Ota"), ("ona", "Ona")]
    registered = models.BooleanField("Ro'yxatdan o'tgan", default=False)
    parent_type = models.CharField("Kim", max_length=4, choices=PARENT_TYPES, default="ota")
    parent_first_name = models.CharField("Ota-ona ismi", max_length=80, blank=True)
    parent_last_name = models.CharField("Ota-ona familiyasi", max_length=80, blank=True)
    parent_age = models.PositiveSmallIntegerField("Yoshi", null=True, blank=True)
    parent_workplace = models.CharField("Ish joyi", max_length=120, blank=True)
    parent_email = models.EmailField("Email (Gmail)", blank=True)
    child_first_name = models.CharField("Bola ismi", max_length=80, blank=True)
    child_last_name = models.CharField("Bola familiyasi", max_length=80, blank=True)

    daily_limit_minutes = models.PositiveSmallIntegerField(
        "Kunlik vaqt chegarasi (daqiqa)", default=60
    )
    weekly_goal_minutes = models.PositiveSmallIntegerField(
        "Haftalik maqsad (daqiqa)", default=180
    )
    bedtime_start = models.TimeField("Tunlik bloklash boshlanishi", default=time(21, 0))
    bedtime_end = models.TimeField("Tunlik bloklash tugashi", default=time(7, 0))

    # Kategoriyalar bo'yicha ruxsat
    allow_mental = models.BooleanField("Mental arifmetika", default=True)
    allow_xotira = models.BooleanField("Xotira", default=True)
    allow_tezoqish = models.BooleanField("Tez o'qish", default=True)
    allow_diqqat = models.BooleanField("Diqqat", default=True)
    allow_matematika = models.BooleanField("Matematika", default=True)

    is_blocked = models.BooleanField("Hisob bloklangan", default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ota-ona nazorati"
        verbose_name_plural = "Ota-ona nazorati"

    def __str__(self):
        return f"{self.user} nazorati"

    def is_category_allowed(self, category_slug: str) -> bool:
        mapping = {
            "mental": self.allow_mental,
            "xotira": self.allow_xotira,
            "tezoqish": self.allow_tezoqish,
            "diqqat": self.allow_diqqat,
            "matematika": self.allow_matematika,
        }
        return mapping.get(category_slug, True)

    def is_within_bedtime(self) -> bool:
        now = timezone.localtime().time()
        start, end = self.bedtime_start, self.bedtime_end
        if start > end:  # tun yarmidan o'tadigan oraliq
            return start <= now or now < end
        return start <= now < end
