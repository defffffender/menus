"""Клиент Eskiz.uz (SMS-шлюз).

Поток: авторизуемся по email/паролю кабинета → получаем JWT-токен (живёт ~30
дней) → шлём SMS с заголовком Authorization: Bearer. Токен кешируем, при 401
(протух) перелогиниваемся и повторяем один раз.

Важно про модерацию: текст SMS должен быть заранее одобрен в кабинете Eskiz.
До модерации шлюз принимает только согласованный тестовый текст. Брендовый
отправитель (ник вместо '4546') тоже регистрируется и модерируется отдельно.
"""
import logging

import requests
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger('sms')

_TOKEN_CACHE_KEY = 'eskiz:token'
_TOKEN_TTL = 60 * 60 * 24 * 20  # 20 дней (с запасом до 30-дневного протухания)
_TIMEOUT = 15


class EskizError(Exception):
    pass


def _digits(phone):
    """Eskiz ждёт номер в виде 998XXXXXXXXX — только цифры, без «+»."""
    return ''.join(ch for ch in str(phone or '') if ch.isdigit())


def _login():
    """Получить новый токен по логину/паролю кабинета и положить в кеш."""
    if not settings.ESKIZ_EMAIL or not settings.ESKIZ_PASSWORD:
        raise EskizError('ESKIZ_EMAIL/ESKIZ_PASSWORD не заданы')
    resp = requests.post(
        f'{settings.ESKIZ_BASE_URL}/auth/login',
        data={'email': settings.ESKIZ_EMAIL, 'password': settings.ESKIZ_PASSWORD},
        timeout=_TIMEOUT,
    )
    resp.raise_for_status()
    token = (resp.json().get('data') or {}).get('token')
    if not token:
        raise EskizError(f'Eskiz не вернул токен: {resp.text[:200]}')
    cache.set(_TOKEN_CACHE_KEY, token, _TOKEN_TTL)
    return token


def _token(force=False):
    if not force:
        cached = cache.get(_TOKEN_CACHE_KEY)
        if cached:
            return cached
    return _login()


def send(phone, text, sender=None):
    """Отправить SMS. Возвращает разобранный JSON ответа Eskiz или бросает.

    При 401 (токен протух) — один перелогин и повтор.
    """
    payload = {
        'mobile_phone': _digits(phone),
        'message': text,
        'from': sender or settings.ESKIZ_FROM,
    }
    url = f'{settings.ESKIZ_BASE_URL}/message/sms/send'

    token = _token()
    resp = requests.post(url, data=payload,
                         headers={'Authorization': f'Bearer {token}'}, timeout=_TIMEOUT)
    if resp.status_code == 401:
        token = _token(force=True)
        resp = requests.post(url, data=payload,
                             headers={'Authorization': f'Bearer {token}'}, timeout=_TIMEOUT)

    if resp.status_code >= 400:
        raise EskizError(f'Eskiz {resp.status_code}: {resp.text[:300]}')
    return resp.json()
