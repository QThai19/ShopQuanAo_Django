from django import template
from decimal import Decimal

register = template.Library()


@register.filter
def vnd(value):
    """Format a number as Vietnamese currency: 360.000 đ"""
    try:
        number = int(Decimal(str(value)))
        formatted = f"{number:,}".replace(",", ".")
        return f"{formatted} đ"
    except (ValueError, TypeError):
        return value
