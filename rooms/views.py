from math import ceil
from django.shortcuts import render
from django.core.paginator import Paginator
from . import models


def all_rooms(request):
    page = request.GET.get("potato", 1)
    potato = int(page or 1)
    page_size = 10
    limit = page_size * potato
    offset = limit - page_size
    all_rooms = models.Room.objects.all()[offset:limit]
    page_count = ceil(models.Room.objects.count() / page_size)
    return render(
        request,
        "rooms/home.html",
        {
            "rooms": all_rooms,
            "page_count": page_count,
            "page": potato,
            "page_range": range(1, page_count),
        },
    )
