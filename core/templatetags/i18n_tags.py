"""Til tarjimasi uchun oddiy filter: {{ T|tr:"kalit" }}."""

from django import template

register = template.Library()


@register.filter
def tr(table, key):
    try:
        return table.get(key, key)
    except Exception:
        return key
