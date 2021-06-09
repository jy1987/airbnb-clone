from django.utils import timezone
from django.views.generic import ListView
from django.urls import reverse
from django.shortcuts import render, redirect
from . import models


class HomeView(ListView):

    model = models.Room
    paginate_by = 10
    ordering = "name"
    context_object_name = "rooms"


def room_detail(request, pk):
    try:
        room = models.Room.objects.get(pk=pk)
        print(room)
        return render(request, "rooms/detail.html", {"room": room})
    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))
