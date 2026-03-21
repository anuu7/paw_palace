from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Access a dictionary item by key in a Django template."""
    if dictionary is None:
        return []
    return dictionary.get(key, [])
