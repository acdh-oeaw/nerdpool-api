from django import template

register = template.Library()

@register.filter
def to_underline(value):
    return value.replace(" ","_")
