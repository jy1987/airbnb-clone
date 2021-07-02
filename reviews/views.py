from django.shortcuts import render, redirect, reverse
from . import forms
from rooms import models as room_models
from . import models

# Create your views here.
def create_review(request, pk):
    user = request.user
    if user.is_authenticated:
        if request.method == "POST":
            form = forms.CreateReviewForm(request.POST)

            if form.is_valid():
                try:
                    room = room_models.Room.objects.get(pk=pk)
                    review = form.save()
                    review.user = request.user
                    review.room = room
                    review.save()
                    return redirect(reverse("rooms:detail", kwargs={"pk": pk}))
                except room_models.Room.DoesNotExist:
                    return redirect(reverse("core:home"))


def delete_review(request, pk, room_pk):
    user = request.user
    review = models.Review.objects.get(pk=pk)
    print(review.pk)
    review_user = review.user
    if user == review_user:
        review.delete()
        return redirect(reverse("rooms:detail", kwargs={"pk": room_pk}))
    else:
        return redirect(reverse("rooms:detail", kwargs={"pk": room_pk}))
