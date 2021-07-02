from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("create/<int:pk>", views.create_review, name="create"),
    path("<int:room_pk>/delete_review/<int:pk>", views.delete_review, name="delete"),
]
