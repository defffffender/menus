"""Отправка SMS.

ESKIZ_ENABLED=True → шлём через Eskiz.uz. Иначе (dev) — код пишется в лог/консоль.
Если реальная отправка упала: в DEBUG не роняем UX (логируем + печатаем код в
консоль, чтобы продолжить отладку), в проде — пробрасываем ошибку выше.
"""
import logging

from django.conf import settings

logger = logging.getLogger('sms')


def _log_stub(phone, text):
    logger.warning('SMS → %s: %s', phone, text)
    print(f'[SMS] {phone}: {text}')  # видно код при разработке


def send_sms(phone, text):
    if getattr(settings, 'ESKIZ_ENABLED', False):
        try:
            from .eskiz import send as eskiz_send
            result = eskiz_send(phone, text)
            logger.info('Eskiz sent to %s: %s', phone, result)
            return
        except Exception:
            logger.exception('Eskiz send failed for %s', phone)
            if not settings.DEBUG:
                raise  # на проде не глотаем — пусть вызывающий знает
    _log_stub(phone, text)
