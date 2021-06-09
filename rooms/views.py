from django.utils import timezone
from django.views.generic import ListView
from . import models


class HomeView(ListView):

    model = models.Room
    paginate_by = 10
    ordering = "name"
    context_object_name = "rooms"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # super()가 없으면 모든 데이터가 사라진다.
        now = timezone.now()
        context["now"] = now  # template 안에 context 추가하는 방법
        return context
