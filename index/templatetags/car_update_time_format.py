from django import template
import time

register = template.Library()


@register.filter
def car_update_time_format(value):
    time_string = value.strftime("%Y-%m-%d")
    return time_string
