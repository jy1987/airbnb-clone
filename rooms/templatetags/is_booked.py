from django import template

register = template.Library()


@register.simple_tag
def is_booked(room, num):
    print(room, num)
    return True
