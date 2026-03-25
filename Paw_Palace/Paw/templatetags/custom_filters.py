from django import template

register = template.Library()

@register.filter
def status_badge(value):
    """Convert status string to a CSS-safe badge class name (keeps underscores for class matching)."""
    if not value:
        return 'pending'
    return value.lower().replace(' ', '-')

@register.filter
def status_label(value):
    """Convert status string to a human-readable label with proper capitalization."""
    if not value:
        return 'Pending'
    labels = {
        'pending': 'Pending',
        'confirmed': 'Confirmed',
        'dispatched': 'Dispatched',
        'shipped': 'Shipped',
        'out_for_delivery': 'Out for Delivery',
        'delivered': 'Delivered',
        'cancelled': 'Cancelled',
        'completed': 'Completed',
    }
    return labels.get(value.lower(), value.replace('_', ' ').title())

@register.filter
def status_css_class(value):
    """Convert status to CSS class name (replaces underscores with hyphens)."""
    if not value:
        return 'pending'
    return value.lower().replace('_', '-')
