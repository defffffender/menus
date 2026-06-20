"""Проверка интеграции Eskiz: отправляет тестовую SMS на указанный номер.

Использование:
    python manage.py eskiz_test +998901234567
    python manage.py eskiz_test +998901234567 "Menus: код подтверждения 1234"

До модерации текста в кабинете Eskiz шлюз принимает только согласованный
тестовый текст — иначе вернёт ошибку модерации.
"""
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Отправить тестовую SMS через Eskiz на указанный номер'

    def add_arguments(self, parser):
        from apps.accounts.services import OTP_MESSAGES
        parser.add_argument('phone', help='Номер в формате +998XXXXXXXXX')
        # по умолчанию — реальный промодерированный шаблон регистрации с примером кода
        parser.add_argument('message', nargs='?',
                            default=OTP_MESSAGES['register'].format(code='1234'),
                            help='Текст сообщения (по умолчанию — шаблон регистрации)')

    def handle(self, *args, **opts):
        if not settings.ESKIZ_ENABLED:
            self.stdout.write(self.style.WARNING(
                'ESKIZ_ENABLED=False — реальная отправка выключена. '
                'Включите в .env (ESKIZ_ENABLED=True) и задайте ESKIZ_EMAIL/ESKIZ_PASSWORD.'))
        from apps.accounts.eskiz import EskizError, send
        try:
            result = send(opts['phone'], opts['message'])
        except EskizError as e:
            raise CommandError(f'Eskiz error: {e}')
        except Exception as e:  # сетевые/HTTP ошибки
            raise CommandError(f'Не удалось отправить: {e}')
        self.stdout.write(self.style.SUCCESS(f'Отправлено. Ответ Eskiz: {result}'))
