from django.shortcuts import render, redirect, reverse
from rooms import models as room_models
from . import models

# Create your views here.
def add(request, room_pk):
    try:
        room = room_models.Room.objects.get(pk=room_pk)
        if room is not None:
            fav_list, created = models.List.objects.get_or_create(
                user=request.user, name="Hope"
            )
            fav_list.rooms.add(room)
        return redirect(reverse("rooms:detail", kwargs={"pk": room_pk}))
    except room_models.Room.DoesNotExist:
        return redirect(reverse("core:home"))
