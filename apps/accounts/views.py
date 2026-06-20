from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render

from apps.core.translations import tr
from apps.restaurants.models import Membership, Restaurant
from apps.restaurants.utils import unique_slug

from .models import User, is_valid_uz_phone, normalize_phone
from .services import attempts_left, issue_otp, otp_cooldown, verify_otp

AUTH_BACKEND = 'django.contrib.auth.backends.ModelBackend'


def register(request):
    # уже вошёл — новое заведение добавляется из кабинета, не через регистрацию
    if request.user.is_authenticated:
        return redirect('restaurants:cabinet')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        rtype = request.POST.get('type', '').strip() or Restaurant.Type.RESTAURANT
        city = request.POST.get('city', '').strip()
        phone = request.POST.get('phone', '').strip()
        nphone = normalize_phone(phone)
        if not name or not phone:
            messages.error(request, tr(request, 'err_required'))
        elif not is_valid_uz_phone(phone):
            messages.error(request, tr(request, 'err_phone_uz'))
        elif User.objects.filter(phone=nphone).exists():
            # один номер — один аккаунт; новые заведения добавляются в кабинете
            messages.error(request, tr(request, 'reg_exists'))
            return redirect('accounts:login')
        else:
            request.session['reg_data'] = {'name': name, 'type': rtype, 'city': city, 'phone': phone}
            request.session['otp_phone'] = nphone
            request.session['otp_mode'] = 'register'
            if otp_cooldown(nphone):
                messages.info(request, tr(request, 'err_otp_throttled'))
            else:
                issue_otp(phone)
                messages.success(request, tr(request, 'msg_code_sent'))
            return redirect('accounts:verify')
    return render(request, 'accounts/register.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('restaurants:cabinet')
    if request.method == 'POST':
        phone = request.POST.get('phone', '').strip()
        nphone = normalize_phone(phone)
        if not is_valid_uz_phone(phone):
            messages.error(request, tr(request, 'err_phone_uz'))
        elif not User.objects.filter(phone=nphone).exists():
            messages.error(request, tr(request, 'err_no_user'))
        else:
            request.session['otp_phone'] = nphone
            request.session['otp_mode'] = 'login'
            if otp_cooldown(nphone):
                messages.info(request, tr(request, 'err_otp_throttled'))
            else:
                issue_otp(phone)
                messages.success(request, tr(request, 'msg_code_sent'))
            return redirect('accounts:verify')
    return render(request, 'accounts/login.html')


def verify(request):
    if request.user.is_authenticated:
        return redirect('restaurants:cabinet')
    phone = request.session.get('otp_phone')
    mode = request.session.get('otp_mode')
    if not phone or not mode:
        return redirect('accounts:login')

    if request.method == 'POST':
        code = request.POST.get('code', '').strip()
        result = verify_otp(phone, code)

        if result == 'ok':
            if mode == 'register':
                data = request.session.get('reg_data', {})
                user, _ = User.objects.get_or_create(phone=phone)
                restaurant = Restaurant.objects.create(
                    owner=user,
                    name=data.get('name', 'Заведение'),
                    slug=unique_slug(data.get('name', 'menu')),
                    type=data.get('type', Restaurant.Type.RESTAURANT),
                    city=data.get('city', ''),
                    phone=phone,
                )
                Membership.objects.get_or_create(
                    user=user, restaurant=restaurant,
                    defaults={'role': Membership.Role.OWNER},
                )
            else:
                user = User.objects.filter(phone=phone).first()
                if user is None:
                    messages.error(request, tr(request, 'err_no_user'))
                    return redirect('accounts:login')

            login(request, user, backend=AUTH_BACKEND)
            for key in ('otp_phone', 'otp_mode', 'reg_data'):
                request.session.pop(key, None)
            return redirect('restaurants:cabinet')

        # неуспех: блокировка / истёк / неверный — для locked/none уводим к запросу нового кода
        if result in ('locked', 'none'):
            request.session.pop('otp_phone', None)
            messages.error(request, tr(request, 'err_otp_locked' if result == 'locked' else 'err_otp_expired'))
            return redirect('accounts:login' if mode == 'login' else 'accounts:register')

        left = attempts_left(phone)
        messages.error(request, f"{tr(request, 'err_invalid_code')} · {tr(request, 'err_attempts_left')}: {left}")

    # сколько секунд до возможности отправить код заново (для таймера на странице);
    # сервер всё равно проверяет паузу при resend, таймер — только подсказка
    return render(request, 'accounts/verify.html', {'phone': phone, 'resend_in': min(otp_cooldown(phone), 60)})


def resend(request):
    """Повторно отправить код, уважая паузу/лимит. Без перезапроса номера."""
    phone = request.session.get('otp_phone')
    mode = request.session.get('otp_mode')
    if not phone or not mode:
        return redirect('accounts:login')
    if otp_cooldown(phone):
        messages.info(request, tr(request, 'err_otp_throttled'))
    else:
        issue_otp(phone)
        messages.success(request, tr(request, 'msg_code_sent'))
    return redirect('accounts:verify')


def logout_view(request):
    logout(request)
    return redirect('/')
