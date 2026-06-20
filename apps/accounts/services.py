import random
from datetime import timedelta

from django.utils import timezone

from .models import PhoneOTP, normalize_phone
from .sms import send_sms

OTP_LENGTH = 4
OTP_TTL = timedelta(minutes=5)
# защита от злоупотреблений
OTP_RESEND_PAUSE = timedelta(seconds=60)   # не чаще одного кода в минуту на номер
OTP_HOURLY_LIMIT = 5                        # не больше N кодов в час на номер
OTP_MAX_ATTEMPTS = 5                        # после N неверных вводов код сгорает


def otp_cooldown(phone):
    """Сколько секунд ждать перед новым кодом (0 — можно отправлять).

    Пауза действует только пока есть «живой» (неиспользованный) код — это гасит
    SMS-бомбинг, но не запирает пользователя после сжигания/успеха. Сверху —
    часовой лимит на номер.
    """
    phone = normalize_phone(phone)
    now = timezone.now()
    pending = (
        PhoneOTP.objects
        .filter(phone=phone, is_used=False)
        .order_by('-created_at')
        .first()
    )
    if pending:
        elapsed = now - pending.created_at
        if elapsed < OTP_RESEND_PAUSE:
            return int((OTP_RESEND_PAUSE - elapsed).total_seconds()) + 1
    hour_ago = now - timedelta(hours=1)
    if PhoneOTP.objects.filter(phone=phone, created_at__gte=hour_ago).count() >= OTP_HOURLY_LIMIT:
        return int(OTP_TTL.total_seconds())  # сигнал «лимит исчерпан»
    return 0


def issue_otp(phone):
    """Сгенерировать код, сохранить и «отправить» по SMS."""
    phone = normalize_phone(phone)
    code = f'{random.randint(0, 10 ** OTP_LENGTH - 1):0{OTP_LENGTH}d}'
    PhoneOTP.objects.create(phone=phone, code=code)
    send_sms(phone, f'Menus: код подтверждения {code}')
    return code


def verify_otp(phone, code):
    """Проверить код. Возвращает статус:

    'ok'     — код верный, вход разрешён;
    'bad'    — неверный код, попытки ещё остались;
    'locked' — исчерпан лимит попыток, код сожжён (нужен новый);
    'none'   — нет активного кода (не запрашивали или истёк).
    """
    phone = normalize_phone(phone)
    otp = (
        PhoneOTP.objects
        .filter(phone=phone, is_used=False)
        .order_by('-created_at')
        .first()
    )
    if otp is None:
        return 'none'
    if timezone.now() - otp.created_at > OTP_TTL:
        otp.is_used = True
        otp.save(update_fields=['is_used'])
        return 'none'

    otp.attempts += 1
    if otp.code == (code or '').strip():
        otp.is_used = True
        otp.save(update_fields=['is_used', 'attempts'])
        return 'ok'
    # неверный код
    if otp.attempts >= OTP_MAX_ATTEMPTS:
        otp.is_used = True  # сжигаем после лимита попыток
        otp.save(update_fields=['attempts', 'is_used'])
        return 'locked'
    otp.save(update_fields=['attempts'])
    return 'bad'


def attempts_left(phone):
    """Сколько неверных попыток осталось для текущего кода (для подсказки)."""
    phone = normalize_phone(phone)
    otp = (
        PhoneOTP.objects
        .filter(phone=phone, is_used=False)
        .order_by('-created_at')
        .first()
    )
    if otp is None:
        return 0
    return max(0, OTP_MAX_ATTEMPTS - otp.attempts)
