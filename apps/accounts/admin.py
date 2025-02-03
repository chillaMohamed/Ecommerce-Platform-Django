
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {"fields": (
                "first_name",
                "last_name",
                "phone",
                "country")
            }
        ),
        (
            _("Permissions"),
            {"fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
            },
        ),
        (
            _("Important dates"),
            {"fields": ("last_login", "date_joined")}
        ),
    )

    list_display = ("username", "full_name", "is_staff","is_active", "date_joined")
    search_fields = ( "first_name", "last_name")
    ordering = ("date_joined",)



