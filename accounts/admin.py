"""accounts admin sozlamalari."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import ParentalControl, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "full_name", "age_group", "level", "xp", "coins", "stars", "streak_days", "is_active")
    list_filter = ("age_group", "is_active", "is_staff")
    search_fields = ("username", "full_name")
    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "BrainGames profili",
            {
                "fields": (
                    "full_name", "age_group", "avatar",
                    "xp", "coins", "stars", "streak_days",
                    "last_active", "sound_enabled", "language",
                )
            },
        ),
    )

    @admin.display(description="Daraja")
    def level(self, obj):
        return obj.level


@admin.register(ParentalControl)
class ParentalControlAdmin(admin.ModelAdmin):
    list_display = ("user", "is_enabled", "daily_limit_minutes", "is_blocked", "updated_at")
    list_filter = ("is_enabled", "is_blocked")
    search_fields = ("user__username", "user__full_name")
