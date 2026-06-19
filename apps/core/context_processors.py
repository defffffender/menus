from .translations import i18n_context, resolve_lang


def i18n(request):
    # {{ t.key }}, {{ LANG }}, {{ LANGUAGES }} в шаблонах
    return i18n_context(resolve_lang(request))
