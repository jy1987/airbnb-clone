from django.contrib import admin
from django.utils.html import mark_safe
from . import models

# Register your models here.
# 각각 가져야할 조건이나 속성들이 다르므로 세개로 나눴다.


@admin.register(models.RoomType, models.HouseRule, models.Amenity, models.Facility)
class ItemAdmin(admin.ModelAdmin):
    """Item Admin definition"""

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()

    pass


class PhotoInline(admin.TabularInline):
    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    """Room Admin definition"""

    inlines = (PhotoInline,)

    fieldsets = (
        (
            "basic Info",
            {"fields": ("name", "description", "country", "city", "price", "address")},
        ),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")}),
        ("Spaces", {"fields": ("guests", "beds", "bedrooms", "baths")}),
        (
            "More About the Space",
            {
                "classes": ("collapse",),  # => 필요에 따라 접거나 펴서 보이게끔 해주는 옵션
                "fields": ("amenities", "facilities", "house_rules"),
            },
        ),
        ("Last Details", {"fields": ("host",)}),
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",  # 1 def
        "count_photos",
        "total_rating",
    )

    list_filter = (
        "instant_book",
        "host__superhost",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )

    raw_id_fields = ("host",)

    ordering = ("name",)

    search_fields = ("=city", "^host__username")

    filter_horizontal = ("amenities", "facilities", "house_rules")

    def count_amenities(
        self, obj
    ):  # 1 함수 이름과 list 이름이 같아야함. obj 는 row를 말하며, 여기선 Room 이다.
        return obj.amenities.count()  # Room에서 __str__ 로 name을 리턴했으므로 Room.name이 출력됨.

    count_amenities.short_description = "amenities"  # 이름 바꿀 수 있음

    def count_photos(self, obj):
        return obj.photos.count()


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """Photo Admin definition"""

    list_display = (
        "__str__",
        "get_thumbnail",
        "name_room",
    )

    def get_thumbnail(self, obj):
        return mark_safe(f"<img width=40px src={obj.file.url}/>")

    get_thumbnail.short_description = "thumbnail"
