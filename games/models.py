"""O'yin modellari: o'yin ta'riflari, sessiyalar, urinishlar va progress."""

from django.conf import settings
from django.db import models
from django.utils import timezone


class Game(models.Model):
    """Platformadagi bitta o'yin turi (mental, abakus, tez o'qish, xotira)."""

    slug = models.SlugField("Slug", unique=True)
    title = models.CharField("Nomi", max_length=80)
    category = models.CharField("Kategoriya", max_length=20, blank=True)
    kind = models.CharField("O'yin turi (React)", max_length=20, default="quiz")
    short_title = models.CharField("Qisqa nomi", max_length=40, blank=True)
    tagline = models.CharField("Shior", max_length=160, blank=True)
    description = models.TextField("Tavsif", blank=True)
    skill = models.CharField("Ko'nikma", max_length=80, blank=True)
    icon = models.CharField("Belgi (emoji)", max_length=8, default="🎮")
    color = models.CharField("Asosiy rang", max_length=20, default="#14b8a6")
    color_2 = models.CharField("Ikkilamchi rang", max_length=20, default="#0ea5e9")
    order = models.PositiveSmallIntegerField("Tartib", default=0)
    is_active = models.BooleanField("Faol", default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "O'yin"
        verbose_name_plural = "O'yinlar"

    def __str__(self):
        return self.title


class Progress(models.Model):
    """Foydalanuvchining bitta o'yindagi umumiy progressi (adaptiv holat)."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="progress",
    )
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="progress")
    difficulty = models.PositiveSmallIntegerField("Joriy daraja", default=1)
    best_score = models.PositiveIntegerField("Eng yaxshi natija", default=0)
    total_sessions = models.PositiveIntegerField("Sessiyalar", default=0)
    total_questions = models.PositiveIntegerField("Savollar", default=0)
    total_correct = models.PositiveIntegerField("To'g'ri javoblar", default=0)
    total_seconds = models.PositiveIntegerField("Sarflangan vaqt (s)", default=0)
    streak = models.SmallIntegerField("Joriy ketma-ketlik", default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "game")
        verbose_name = "Progress"
        verbose_name_plural = "Progress"

    def __str__(self):
        return f"{self.user} · {self.game} · daraja {self.difficulty}"

    @property
    def accuracy(self):
        if not self.total_questions:
            return 0
        return round(self.total_correct / self.total_questions * 100)

    @property
    def minutes(self):
        return round(self.total_seconds / 60)


class GameSession(models.Model):
    """Bitta o'ynalgan sessiya."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sessions",
    )
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="sessions")
    score = models.PositiveIntegerField("Ball", default=0)
    coins_earned = models.PositiveIntegerField("Yutilgan tangalar", default=0)
    xp_earned = models.PositiveIntegerField("Yutilgan XP", default=0)
    stars_earned = models.PositiveIntegerField("Yutilgan yulduzlar", default=0)
    questions_total = models.PositiveIntegerField("Jami savollar", default=0)
    questions_correct = models.PositiveIntegerField("To'g'ri javoblar", default=0)
    duration_seconds = models.PositiveIntegerField("Davomiyligi (s)", default=0)
    difficulty_start = models.PositiveSmallIntegerField("Boshlang'ich daraja", default=1)
    difficulty_end = models.PositiveSmallIntegerField("Yakuniy daraja", default=1)
    created_at = models.DateTimeField("Sana", default=timezone.now)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Sessiya"
        verbose_name_plural = "Sessiyalar"

    def __str__(self):
        return f"{self.user} · {self.game} · {self.score} ball"

    @property
    def accuracy(self):
        if not self.questions_total:
            return 0
        return round(self.questions_correct / self.questions_total * 100)


class Attempt(models.Model):
    """Sessiya ichidagi bitta savol-javob urinishi."""

    session = models.ForeignKey(
        GameSession, on_delete=models.CASCADE, related_name="attempts"
    )
    prompt = models.CharField("Savol", max_length=200)
    correct_answer = models.CharField("To'g'ri javob", max_length=120)
    user_answer = models.CharField("Foydalanuvchi javobi", max_length=120, blank=True)
    is_correct = models.BooleanField("To'g'ri", default=False)
    difficulty = models.PositiveSmallIntegerField("Daraja", default=1)
    time_ms = models.PositiveIntegerField("Sarflangan vaqt (ms)", default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "Urinish"
        verbose_name_plural = "Urinishlar"

    def __str__(self):
        return f"{self.prompt} = {self.user_answer} ({'✓' if self.is_correct else '✗'})"


class Achievement(models.Model):
    """Bola qo'lga kiritishi mumkin bo'lgan yutuq (nishon)."""

    code = models.SlugField("Kod", unique=True)
    title = models.CharField("Nomi", max_length=80)
    description = models.CharField("Tavsif", max_length=160)
    icon = models.CharField("Belgi", max_length=8, default="🏅")
    coins = models.PositiveIntegerField("Mukofot tangalar", default=50)

    class Meta:
        verbose_name = "Yutuq"
        verbose_name_plural = "Yutuqlar"

    def __str__(self):
        return self.title


class UserAchievement(models.Model):
    """Foydalanuvchi qo'lga kiritgan yutuq."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="achievements",
    )
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "achievement")
        ordering = ["-earned_at"]

    def __str__(self):
        return f"{self.user} → {self.achievement}"
