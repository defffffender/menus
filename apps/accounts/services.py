import random
from datetime import timedelta

from django.utils import timezone

from .models import PhoneOTP, normalize_phone
from .sms import send_sms

OTP_LENGTH = 4
OTP_TTL = timedelta(minutes=5)


def issue_otp(phone):
    """Сгенерировать код, сохранить и «отправить» по SMS."""
    phone = normalize_phone(phone)
    code = f'{random.randint(0, 10 ** OTP_LENGTH - 1):0{OTP_LENGTH}d}'
    PhoneOTP.objects.create(phone=phone, code=code)
    send_sms(phone, f'Menus: код подтверждения {code}')
    return code


def verify_otp(phone, code):
    """Проверить код: не использован, не просрочен, совпадает."""
    phone = normalize_phone(phone)
    otp = (
        PhoneOTP.objects
        .filter(phone=phone, is_used=False)
        .order_by('-created_at')
        .first()
    )
    if otp is None:
        return False
    if timezone.now() - otp.created_at > OTP_TTL:
        return False
    otp.attempts += 1
    if otp.code != (code or '').strip():
        otp.save(update_fields=['attempts'])
        return False
    otp.is_used = True
    otp.save(update_fields=['is_used', 'attempts'])
    return True
