from django.contrib import messages
from django.http.response import Http404
from django.views.generic import ListView, DetailView, View, UpdateView, CreateView
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView, FormView
from django_countries import countries
from django.urls import reverse
from users import mixins as user_mixins
from django.shortcuts import render, redirect
from . import models, forms


class HomeView(ListView):

    model = models.Room
    paginate_by = 12
    ordering = "name"
    context_object_name = "rooms"


class RoomDetail(DetailView):

    model = models.Room


class SearchView(View):
    def get(self, request):

        country = request.GET.get("country")

        if country:

            form = forms.SearchForm(request.GET)

            if form.is_valid():

                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                print(filter_args)

                qs = models.Room.objects.filter(**filter_args)

                for amenity in amenities:
                    qs = qs.filter(amenities=amenity)

                for facility in facilities:
                    qs = qs.filter(facilities=facility)

                qs = qs.order_by("created")

                paginator = Paginator(qs, 2)

                url = request.get_full_path()

                page = request.GET.get("page", 1)

                rooms = paginator.get_page(page)

                print(page)

                return render(
                    request,
                    "rooms/search.html",
                    {"form": form, "rooms": rooms, "url": url},
                )

        else:

            form = forms.SearchForm()

        return render(request, "rooms/search.html", {"form": form})


class EditRoomView(user_mixins.LoggedInOnlyView, UpdateView):

    model = models.Room
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        print(room.host.pk, self.request.user.pk)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


class RoomPhotosView(user_mixins.LoggedInOnlyView, DetailView):

    model = models.Room
    template_name = "rooms/room_photo.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        print(room.host.pk, self.request.user.pk)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


@login_required
def delete_photo(request, room_pk, photo_pk):
    user = request.user
    try:
        room = models.Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(request, "Can't edit photo")
        else:
            photo = models.Photo.objects.get(pk=photo_pk)
            # photo = request.GET.get(models.Room, photo_pk) : pk를 불러온다.
            # request 로 요청하기 때문에
            photo.delete()
            messages.success(request, "deleted that photo")
        return redirect(reverse("rooms:edit-photo", kwargs={"pk": room_pk}))
    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))


class EditPhotoView(user_mixins.LoggedInOnlyView, UpdateView):

    model = models.Photo
    pk_url_kwarg = "photo_pk"
    fields = (
        "caption",
        "file",
    )

    def get_success_url(self):

        room_pk = self.kwargs.get("room_pk")
        return reverse("rooms:edit-photo", kwargs={"pk": room_pk})


class AddPhotoView(user_mixins.LoggedInOnlyView, CreateView):
    model = models.Photo
    template_name = "rooms/add_photo.html"
    fields = (
        "caption",
        "file",
        "room",
    )

    def get_success_url(self):

        room_pk = self.kwargs.get("pk")
        return reverse("rooms:edit-photo", kwargs={"pk": room_pk})

    # def form_valid(self, form):

    #     pk = self.kwargs.get("pk")  # view는 pk를 알고 있다.

    #     form.save(pk)
    #     return redirect(reverse("rooms:edit-photo", kwargs={"pk": pk}))


# class AddPhotoView(user_mixins.LoggedInOnlyView, FormView):

#     template_name = "rooms/add_photo.html"
#     form_class = forms.CreatePhotoForm

#     def form_valid(self, form):
#         pk = self.kwargs.get("pk")  # view는 pk를 알고 있다.
#         form.save(pk)
#         return redirect(reverse("rooms:edit-photo", kwargs={"pk": pk}))


class CreateRoomView(user_mixins.LoggedInOnlyView, CreateView):
    model = models.Room
    template_name = "rooms/room_create.html"
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "host",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )

    def form_valid(self, form):
        room = form.save()  # room은 form이 save된 형태
        room.host = self.request.user
        room.save()
        return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))
