# your_app/templatetags/custom_filters.py
from django import template # type: ignore

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
