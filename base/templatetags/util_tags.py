from django import template

register = template.Library()


@register.filter(name='value_or_na')
def check(value):
    if value:
        return value
    return 'NA'
