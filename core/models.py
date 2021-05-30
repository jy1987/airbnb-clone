from django.db import models

# Create your models here.


class TimeStampedModel(models.Model):

    """Time Stamped Model(abstract)"""

    created = models.DateTimeField(auto_now_add=True)  # 처음 만들어진 시간 기록
    updated = models.DateTimeField(auto_now=True)  # 바뀔 때마다 변경되는 시간 기록

    class Meta:  # Meta 는 기타사항을 적음으로써 적용할 수 있음.
        abstract = True  # abstract property : database에 적용 안됨.
