from math import ceil
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from . import models


def all_rooms(request):
    page = request.GET.get("potato", 1)
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10, orphans=5)

    try:
        rooms = paginator.page((page))
        print(vars(rooms))
        print(vars(rooms.paginator))
        return render(
            request,
            "rooms/home.html",
            {"page": rooms},
        )
    except EmptyPage or InvalidPage:
        return redirect("/")
