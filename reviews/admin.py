from core import models
from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    """Review Admin definition"""

    pass
