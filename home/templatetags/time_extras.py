from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def human_time(value):
    if not value:
        return ""

    now = timezone.now()
    diff = now - value

    seconds = int(diff.total_seconds())

    if seconds < 60:
        return "Just now"

    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"

    elif seconds < 86400:
        hours = seconds // 3600
        return f"{hours} hour{'s' if hours != 1 else ''} ago"

    days = diff.days

    if days == 1:
        return "Yesterday"

    elif days < 7:
        return f"{days} day{'s' if days != 1 else ''} ago"

    elif days < 30:
        weeks = days // 7
        return f"{weeks} week{'s' if weeks != 1 else ''} ago"

    elif days < 365:
        months = days // 30
        return f"{months} month{'s' if months != 1 else ''} ago"

    years = days // 365
    return f"{years} year{'s' if years != 1 else ''} ago"