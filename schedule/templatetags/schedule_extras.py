# schedule/templatetags/schedule_extras.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Получить значение из словаря по ключу в шаблоне"""
    return dictionary.get(key, '')

@register.filter
def get_by_id(queryset, id_str):
    """Найти объект по ID в queryset"""
    try:
        return queryset.get(id=int(id_str))
    except:
        return ''