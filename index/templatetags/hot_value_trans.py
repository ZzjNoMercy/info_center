from django import template

register = template.Library()


@register.filter
def hot_value_trans(value):
    return "%.1f" % (value / 10000)
