from django import template

from usage.utils import get_user_by_pk

register = template.Library()


@register.filter(name='value_or_na')
def check(value):
    if value:
        return value
    return 'NA'


@register.filter(name='subscribed')
def check(plan, user):
    user = get_user_by_pk(user.id)
    if user and user.subscriptions.filter(plan__id=plan.id).first():
        return True
    return False


@register.filter(name='divide_by')
def divide_by(num, divisor):
    return int(num / divisor)
