from django import template

register = template.Library()

@register.filter
def divide(value1, value2):
    if value2 == 0:
        return ZeroDivisionError
    return value1 // value2