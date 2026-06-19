from django.utils.text import slugify

from .models import Restaurant

# Кириллица (рус + узб) → латиница, чтобы slug был ASCII и URL не превращался
# в %D1%82%D0%B5… Транслит простой, человекочитаемый.
_TRANSLIT = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
    'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
    # узбекская кириллица
    'ў': 'o', 'қ': 'q', 'ғ': 'g', 'ҳ': 'h', 'ҷ': 'j', 'ё': 'yo',
}


def transliterate(text):
    out = []
    for ch in (text or '').lower():
        out.append(_TRANSLIT.get(ch, ch))
    return ''.join(out)


def unique_slug(name):
    """Уникальный ASCII-slug на основе названия (кириллица транслитерируется)."""
    base = slugify(transliterate(name)) or 'venue'
    slug = base
    i = 2
    while Restaurant.objects.filter(slug=slug).exists():
        slug = f'{base}-{i}'
        i += 1
    return slug
