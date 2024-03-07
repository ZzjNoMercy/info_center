from django import template

register = template.Library()


@register.filter
def percent_format(value):
    return "{:.1%}".format(value)
