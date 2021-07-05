from django import template
from lists import models as list_models

register = template.Library()


@register.simple_tag(takes_context=True)
def on_favs(context, room):
    user = context.request.user
    favs_list = list_models.List.objects.filter(user=user, rooms=room).exists()
    return favs_list
