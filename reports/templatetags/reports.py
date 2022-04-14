"""
Custom report filters for Django templates.
"""

from typing import Dict

from django import template

register: template.Library = template.Library()


@register.filter(name="total_frequency")
def total_frequency(frequencies: Dict[str, int]) -> int:
    """
    Returns the total of a frequency table.
    """
    return sum(frequencies.values())
