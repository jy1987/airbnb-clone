from django.utils import timezone
from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField
from core import models as core_models
from cal import Calendar

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
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption

    def name_room(self):
        return self.room


class Room(core_models.TimeStampedModel):

    """Room Model Definition"""

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField(
        null=True, help_text="how many people will be staying?"
    )
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
    ):  # python ?????? django?????? __str__ ??? class??? ???????????? class??? string?????? ?????? method??????.
        return str(self.name)

    def save(self, *args, **kwargs):
        self.city = self.city.title()
        self.name = self.name.title()
        super().save(*args, **kwargs)

    def get_absolute_url(self):

        return reverse("rooms:detail", kwargs={"pk": self.pk})

    def total_rating(self):
        all_reviews = self.reviews.all()
        # print(all_reviews)
        all_rating = 0
        for review in all_reviews:
            # print(review)
            all_rating += review.rating_average()

        if len(all_reviews) > 0:

            return round(all_rating / len(all_reviews), 2)
        else:
            return 0

    def first_photo(self):
        # photo = self.photos.all()[:1]  # ????????? ?????? ??????????????? value?????? ???????????? ??????
        try:
            (photo,) = self.photos.all()[:1]
            print(photo.file.url)
            print(dir(photo.file))
            return photo.file.url
        except ValueError:
            return None

    def get_photos(self):
        photos = self.photos.all()[1:5]
        return photos

    def get_calendar(self):
        now = timezone.now()
        this_year = now.year
        this_year2 = this_year
        this_month = now.month
        next_month = this_month + 1
        if this_month == 12:
            next_month = 1
            this_year2 = 1
        this_calendar = Calendar(this_year, this_month)
        next_calendar = Calendar(this_year2, next_month)
        return [this_calendar, next_calendar]
