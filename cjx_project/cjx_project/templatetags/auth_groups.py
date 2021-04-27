from django import template
from django.contrib.auth.models import Group 
from django.contrib.admin.templatetags.admin_list import result_list as admin_list_result_list

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name): 
    if user.groups.filter(name = group_name).exists() or user.is_superuser:
        return True 
    return False
