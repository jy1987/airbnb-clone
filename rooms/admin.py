from django.contrib import admin
from . import models

# Register your models here.
# 각각 가져야할 조건이나 속성들이 다르므로 세개로 나눴다.


@admin.register(models.RoomType, models.HouseRule, models.Amenity, models.Facility)
class ItemAdmin(admin.ModelAdmin):
    """Item Admin definition"""

    pass


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    """Room Admin definition"""

    pass


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ """

    pass
