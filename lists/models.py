from django.db import models
from django.db.models.deletion import CASCADE
from core import models as core_models


class List(core_models.TimeStampedModel):

    name = models.CharField(max_length=80)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE
    )  # 다음엔 ManyToMany 로 해보기
    rooms = models.ManyToManyField("rooms.Room", blank=True)

    def __str__(self):
        return f"{self.name} - {self.user.gender} by {self.user}"
