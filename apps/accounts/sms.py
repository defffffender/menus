"""Отправка SMS. Пока заглушка — код пишется в лог/консоль.

TODO (Этап 7): интеграция с Eskiz.uz.
"""
import logging

logger = logging.getLogger('sms')


def send_sms(phone, text):
    logger.warning('SMS → %s: %s', phone, text)
    # дублируем в консоль, чтобы код было видно при разработке
    print(f'[SMS] {phone}: {text}')
