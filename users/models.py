from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db import models
from django.db.models.fields import BLANK_CHOICE_DASH

# Create your models here.
class User(AbstractUser):

    """Custom User Model"""

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICE = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "kr"

    LANGUAGE_CHOICE = ((LANGUAGE_ENGLISH, "English"), (LANGUAGE_KOREAN, "Korean"))

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"

    CURRENCY_CHOICE = ((CURRENCY_USD, "USD"), (CURRENCY_KRW, "KRW"))

    avatar = models.ImageField(upload_to="avatar", blank=True)
    gender = models.CharField(
        choices=GENDER_CHOICE, max_length=10, blank=True
    )  # 단순 form에만 영향을 미침. not database
    bio = models.TextField(
        default="", blank=True
    )  # default 를 줘야 database column 을 채움으로써 문제가 안생김.
    birthday = models.DateField(blank=True, null=True)
    language = models.CharField(
        choices=LANGUAGE_CHOICE, max_length=2, blank=True, default=LANGUAGE_KOREAN
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICE, max_length=3, blank=True, default=CURRENCY_KRW
    )
    # hobby = models.TextField(default="")
    superhost = models.BooleanField(default=False)  # superhost 인지 아닌지

    def get_absolute_url(self):

        return reverse("users:profile", kwargs={"pk": self.pk})
