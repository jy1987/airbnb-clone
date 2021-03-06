import datetime
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from core import models as core_models
from . import managers
import reservations

# Create your models here.


class BetweenDay(core_models.TimeStampedModel):

    day = models.DateField()
    reservation = models.ForeignKey("Reservation", on_delete=CASCADE)

    class Meta:
        verbose_name = "Booked Day"
        verbose_name_plural = "Between Days"

    def __str__(self):
        return str(self.day)


class Reservation(core_models.TimeStampedModel):

    """Reservation Model definition"""

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELED, "Canceled"),
    )

    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    check_in = models.DateField()
    check_out = models.DateField()
    guest = models.ForeignKey(
        "users.User", related_name="reservations", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reservations", on_delete=CASCADE
    )
    objects = managers.CustomReservationManager()

    def __str__(self):
        return f"{self.room}"

    def in_progress(self):
        now = timezone.now().date()
        return now >= self.check_in and now <= self.check_out

    in_progress.boolean = True

    def finished(self):
        now = timezone.now().date()
        return now > self.check_out

    finished.boolean = True

    def save(self, *args, **kwargs):
        if self.pk is None:
            room = self.room
            print(room.pk)
            start = self.check_in
            end = self.check_out
            difference = end - start
            print(difference)
            existing_booked_day = BetweenDay.objects.filter(
                day__range=(start, end), reservation__room=room
            ).exists()

            print(existing_booked_day)
            if existing_booked_day is False:
                super().save(*args, **kwargs)
                for i in range(difference.days + 1):
                    day = start + datetime.timedelta(days=i)
                    print(day)
                    BetweenDay.objects.create(day=day, reservation=self)
                return
        return super().save(*args, **kwargs)
