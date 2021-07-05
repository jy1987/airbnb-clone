from django.db import models
from django.db.models.deletion import CASCADE
from core import models as core_models


class List(core_models.TimeStampedModel):

    name = models.CharField(max_length=80)
    user = models.OneToOneField(
        "users.User", related_name="lists", on_delete=models.CASCADE
    )  # 다음엔 ManyToMany 로 해보기
    rooms = models.ManyToManyField("rooms.Room", related_name="lists", blank=True)

    def __str__(self):
        return f"{self.name} - {self.user.gender} by {self.user}"

    def count_rooms(self):
        return self.rooms.count()

    count_rooms.short_description = " Number of Rooms"
