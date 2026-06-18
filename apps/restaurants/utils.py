from django.utils.text import slugify

from .models import Restaurant


def unique_slug(name):
    """Уникальный slug на основе названия (поддержка кириллицы/латиницы)."""
    base = slugify(name, allow_unicode=True) or 'menu'
    slug = base
    i = 2
    while Restaurant.objects.filter(slug=slug).exists():
        slug = f'{base}-{i}'
        i += 1
    return slug
