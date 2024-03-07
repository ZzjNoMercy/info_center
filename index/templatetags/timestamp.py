from django import template

register = template.Library()


@register.filter
def timestamp(value):
    return int(value.timestamp())
