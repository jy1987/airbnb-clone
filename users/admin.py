from django.contrib import admin
from . import models  # 이렇게 from.import 적는건 같은 폴더 안에 models 를 불러온다는 의미

# Register your models here.
@admin.register(models.User)
class CustomUserAdmin(admin.ModelAdmin):
    pass
