from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import TemplateView

from .translations import LANGUAGES, DEFAULT_LANG


class LandingView(TemplateView):
    template_name = 'landing.html'


def set_language(request):
    """Переключение языка интерфейса (сохраняем в сессии)."""
    lang = request.GET.get('lang', DEFAULT_LANG)
    if lang in dict(LANGUAGES):
        request.session['lang'] = lang
    # next принимаем только как внутренний путь — иначе open redirect (фишинг)
    nxt = request.GET.get('next') or '/'
    if not url_has_allowed_host_and_scheme(nxt, allowed_hosts={request.get_host()},
                                           require_https=request.is_secure()):
        nxt = '/'
    return redirect(nxt)
