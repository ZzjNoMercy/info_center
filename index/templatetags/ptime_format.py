from django import template
import time

register = template.Library()


@register.filter
def ptime_format(value):
    time_string = value.strftime("%m-%d %H:%M")
    return time_string
