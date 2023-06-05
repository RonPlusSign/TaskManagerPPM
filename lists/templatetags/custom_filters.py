from django import template
from django.utils import timezone

register = template.Library()


@register.filter(expects_localtime=True)
def is_expired(value):
    if value is None:
        return False
    try:
        return value < timezone.now()
    except AttributeError:
        return False


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
