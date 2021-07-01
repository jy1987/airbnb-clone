import datetime
from django.contrib import messages
from django.http import Http404
from django.views.generic import CreateView, DetailView, View
from django.shortcuts import render, redirect, reverse
from rooms import models as room_models
from . import models


# Create your views here.
class CreateError(Exception):
    pass


def create(request, room, year, month, day):
    try:
        date = datetime.datetime(year=year, month=month, day=day)
        room = room_models.Room.objects.get(pk=room)
        models.BetweenDay.objects.get(day=date, reservation__room=room)
        raise CreateError()
    except (room_models.Room.DoesNotExist, CreateError):
        messages.error(request, "Can not reserve that room")
        return redirect(reverse("core:home"))
    except models.BetweenDay.DoesNotExist:
        reservation = models.Reservation.objects.create(
            guest=request.user,
            room=room,
            check_in=date,
            check_out=date + datetime.timedelta(days=1),
        )
        return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))


class CreateReservationView(DetailView):
    model = models.Reservation
    template_name = "reservation_detail.html"


""" class ReservationDetailView(View):
    
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        reservation = models.Reservation.objects.get_or_none(pk=pk)
   
        if not reservation or (
            reservation.guest != self.request.user
            and reservation.room.host != self.request.user
        ):
            raise Http404()
        return render(
            self.request, "reservations/detail.html", {"reservation": reservation}
        ) """
