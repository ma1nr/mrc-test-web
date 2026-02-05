from django import template

register = template.Library()

@register.filter
def to_str(value):
    """Преобразует значение в строку"""
    return str(value)

@register.filter
def is_selected(selected_value, compare_value):
    """Проверяет, выбрано ли значение"""
    return str(selected_value) == str(compare_value)

@register.filter
def get_item(dictionary, key):
    if dictionary is None:
        return ''
    return dictionary.get(key, '')
