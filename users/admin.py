from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models  # 이렇게 from.import 적는건 같은 폴더 안에 models 를 불러온다는 의미
from rooms import models as room_models

# Register your models here.


class RoomInline(admin.TabularInline):

    model = room_models.Room


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """Custom User Admin"""

    inlines = (RoomInline,)

    fieldsets = (
        (
            "custom profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthday",
                    "language",
                    "currency",
                    "superhost",
                )
            },
        ),
    ) + UserAdmin.fieldsets

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
    )

    list_filter = UserAdmin.list_filter + ("superhost",)
