from .translations import LANGUAGES, TR, resolve_lang


def i18n(request):
    lang = resolve_lang(request)
    return {
        'LANG': lang,
        'LANGUAGES': LANGUAGES,
        # плоский словарь для шаблонов: {{ t.reg_title }}
        't': {key: entry.get(lang) or entry.get('ru') or key for key, entry in TR.items()},
    }
