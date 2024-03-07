from django import template
import time

register = template.Library()


@register.filter
def promotion_time_format(value):
    time_string = value.strftime("%m-%d")
    return time_string
