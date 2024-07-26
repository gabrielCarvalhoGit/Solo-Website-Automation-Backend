from django import template

register = template.Library()

@register.filter
def is_solo_admin(user):
    return user.groups.filter(name='solo_admin').exists()

@register.filter
def is_resp_empresa(user):
    return user.groups.filter(name='resp_empresa').exists()