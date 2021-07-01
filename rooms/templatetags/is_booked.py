from calendar import month
import datetime
from django import template
from reservations import models as reservation_models

register = template.Library()


@register.simple_tag
def is_booked(room, num):
    if num.number == 0:  # num.number는 class Day의 self number를 말한다.
        return
    try:
        date = datetime.datetime(year=num.year, month=num.month, day=num.number)
        reservation_models.BetweenDay.objects.get(day=date, reservation__room=room)
        # reservation__room=room
        return True
    except reservation_models.BetweenDay.DoesNotExist:
        return False
