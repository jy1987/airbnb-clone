from django.db import models

from django_countries.fields import CountryField
from core import models as core_models

## from users import models as user_models

# Create your models here.


class AbstractItem(core_models.TimeStampedModel):

    """Abstract Item"""

    name = models.CharField(max_length=80)

    class Meta:
        abstract: True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    """Room Type Model definition"""

    class Meta:
        verbose_name = "Room Type"


class Amenity(AbstractItem):

    """Amenity Model definition"""

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):

    """Facility Model definition"""

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):

    """HouseRule Model definition"""

    class Meta:
        verbose_name = "House Rule"


class Photo(core_models.TimeStampedModel):

    """Photo Model definition"""

    caption = models.CharField(max_length=80)
    file = models.ImageField()
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    """Room Model Definition"""

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField(null=True)
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        "users.User", related_name="rooms", on_delete=models.CASCADE
    )
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    def __str__(
        self,
    ):  # python 이나 django에서 __str__ 은 class를 발견하면 class를 string처럼 보는 method이다.
        return str(self.name)

    def total_rating(self):
        all_reviews = self.reviews.all()
        # print(all_reviews)
        all_rating = 0
        for review in all_reviews:
            # print(review)
            all_rating += review.rating_average()

        if len(all_reviews) > 0:
            return all_rating / len(all_reviews)
        else:
            return "not review"
