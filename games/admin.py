"""games admin sozlamalari."""

from django.contrib import admin

from .models import (
    Achievement,
    Attempt,
    Game,
    GameSession,
    Progress,
    UserAchievement,
)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "skill", "order", "is_active")
    list_editable = ("order", "is_active")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "game", "difficulty", "accuracy", "total_sessions", "best_score")
    list_filter = ("game",)
    search_fields = ("user__username", "user__full_name")


class AttemptInline(admin.TabularInline):
    model = Attempt
    extra = 0
    can_delete = False
    readonly_fields = ("prompt", "correct_answer", "user_answer", "is_correct", "difficulty", "time_ms")


@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ("user", "game", "score", "accuracy", "questions_total", "created_at")
    list_filter = ("game", "created_at")
    search_fields = ("user__username", "user__full_name")
    inlines = [AttemptInline]


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ("title", "code", "coins", "icon")


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ("user", "achievement", "earned_at")
    list_filter = ("achievement",)
