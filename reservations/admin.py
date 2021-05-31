from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """Reservation Admin definition"""

    list_display = (
        "room",
        "status",
        "check_in",
        "check_out",
        "guest",
        "in_progress",
        "finished",
    )
