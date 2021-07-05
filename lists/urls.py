from django.urls import path
from . import views

app_name = "lists"

urlpatterns = [
    path("add/<int:room_pk>/", views.add, name="add"),
    path("delete/<int:room_pk>/", views.delete, name="delete"),
]
