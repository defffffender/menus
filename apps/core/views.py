from django.shortcuts import redirect
from django.views.generic import TemplateView

from .translations import LANGUAGES, DEFAULT_LANG


class LandingView(TemplateView):
    template_name = 'landing.html'


def set_language(request):
    """Переключение языка интерфейса (сохраняем в сессии)."""
    lang = request.GET.get('lang', DEFAULT_LANG)
    if lang in dict(LANGUAGES):
        request.session['lang'] = lang
    return redirect(request.GET.get('next') or '/')
