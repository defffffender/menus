from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from apps.core.translations import tr
from apps.restaurants.models import Membership, Restaurant
from apps.restaurants.utils import unique_slug

from .models import Lead, User, is_valid_uz_phone, normalize_phone
from .services import attempts_left, issue_otp, otp_cooldown, verify_otp

AUTH_BACKEND = 'django.contrib.auth.backends.ModelBackend'


def _post_login_redirect(user):
    """Куда отправить после входа: агента — в агентский кабинет."""
    if getattr(user, 'is_agent_user', False):
        return redirect('accounts:agent_dashboard')
    return redirect('restaurants:cabinet')


def _password_error(request, pw, pw2, phone=None):
    """Проверка пароля: непустой, совпадает с повтором, проходит политику Django.
    Возвращает текст ошибки или None, если всё хорошо."""
    if not pw:
        return tr(request, 'err_required')
    if pw != pw2:
        return tr(request, 'err_pw_mismatch')
    probe = User(phone=normalize_phone(phone)) if phone else None
    try:
        validate_password(pw, user=probe)
    except ValidationError as e:
        return ' · '.join(e.messages)
    return None


def register(request):
    """Самостоятельной регистрации нет. Эта страница — форма «Оставить заявку»:
    сохраняем лид, дальше менеджер/агент перезванивает и подключает заведение."""
    if request.user.is_authenticated:
        return _post_login_redirect(request.user)
    values = {}
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()        # имя контакта
        venue = request.POST.get('venue', '').strip()       # название заведения
        city = request.POST.get('city', '').strip()
        phone = request.POST.get('phone', '').strip()
        comment = request.POST.get('comment', '').strip()
        values = {'name': name, 'venue': venue, 'city': city, 'phone': phone, 'comment': comment}

        if not phone:
            messages.error(request, tr(request, 'err_required'))
        elif not is_valid_uz_phone(phone):
            messages.error(request, tr(request, 'err_phone_uz'))
        else:
            Lead.objects.create(
                full_name=name, venue_name=venue, city=city,
                phone=normalize_phone(phone), comment=comment,
            )
            messages.success(request, tr(request, 'lead_sent'))
            return redirect('accounts:login')
    return render(request, 'accounts/register.html', {'values': values})


def login_view(request):
    # Вход по телефону + паролю (без SMS).
    if request.user.is_authenticated:
        return _post_login_redirect(request.user)
    if request.method == 'POST':
        phone = request.POST.get('phone', '').strip()
        pw = request.POST.get('password', '')
        nphone = normalize_phone(phone)
        user = authenticate(request, username=nphone, password=pw)
        if user is not None:
            login(request, user, backend=AUTH_BACKEND)
            return _post_login_redirect(user)
        messages.error(request, tr(request, 'err_bad_credentials'))
        return render(request, 'accounts/login.html', {'phone': phone})
    return render(request, 'accounts/login.html')


def verify(request):
    # Подтверждение SMS-кода: для регистрации и для восстановления пароля.
    if request.user.is_authenticated:
        return redirect('restaurants:cabinet')
    phone = request.session.get('otp_phone')
    mode = request.session.get('otp_mode')
    if not phone or mode not in ('register', 'reset'):
        return redirect('accounts:login')

    if request.method == 'POST':
        code = request.POST.get('code', '').strip()
        result = verify_otp(phone, code)

        if result == 'ok':
            if mode == 'register':
                data = request.session.get('reg_data', {})
                user, _ = User.objects.get_or_create(phone=phone)
                if data.get('password'):
                    user.set_password(data['password'])
                    user.save(update_fields=['password'])
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
                login(request, user, backend=AUTH_BACKEND)
                for key in ('otp_phone', 'otp_mode', 'reg_data'):
                    request.session.pop(key, None)
                return redirect('restaurants:cabinet')

            # mode == 'reset': код верный — пускаем к установке нового пароля
            request.session['reset_phone'] = phone
            for key in ('otp_phone', 'otp_mode'):
                request.session.pop(key, None)
            return redirect('accounts:password_reset_set')

        # неуспех: блокировка / истёк / неверный
        if result in ('locked', 'none'):
            request.session.pop('otp_phone', None)
            messages.error(request, tr(request, 'err_otp_locked' if result == 'locked' else 'err_otp_expired'))
            return redirect('accounts:register' if mode == 'register' else 'accounts:password_reset')

        left = attempts_left(phone)
        messages.error(request, f"{tr(request, 'err_invalid_code')} · {tr(request, 'err_attempts_left')}: {left}")

    return render(request, 'accounts/verify.html', {'phone': phone, 'resend_in': min(otp_cooldown(phone), 60)})


def resend(request):
    """Повторно отправить код (для регистрации/восстановления), уважая паузу/лимит."""
    phone = request.session.get('otp_phone')
    mode = request.session.get('otp_mode')
    if not phone or mode not in ('register', 'reset'):
        return redirect('accounts:login')
    if otp_cooldown(phone):
        messages.info(request, tr(request, 'err_otp_throttled'))
    else:
        issue_otp(phone, mode)  # 'register' или 'reset' — соответствующий текст
        messages.success(request, tr(request, 'msg_code_sent'))
    return redirect('accounts:verify')


def password_reset(request):
    """Восстановление доступа: ввод телефона → отправка SMS-кода."""
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
            request.session['otp_mode'] = 'reset'
            if otp_cooldown(nphone):
                messages.info(request, tr(request, 'err_otp_throttled'))
            else:
                issue_otp(phone, 'reset')
                messages.success(request, tr(request, 'msg_code_sent'))
            return redirect('accounts:verify')
    return render(request, 'accounts/password_reset.html')


def password_reset_set(request):
    """Установка нового пароля. Доступна только после подтверждения кода."""
    if request.user.is_authenticated:
        return redirect('restaurants:cabinet')
    phone = request.session.get('reset_phone')
    if not phone:
        return redirect('accounts:password_reset')
    if request.method == 'POST':
        pw = request.POST.get('password', '')
        pw2 = request.POST.get('password2', '')
        err = _password_error(request, pw, pw2, phone)
        if err:
            messages.error(request, err)
        else:
            user = User.objects.filter(phone=phone).first()
            if user is None:
                request.session.pop('reset_phone', None)
                return redirect('accounts:login')
            user.set_password(pw)
            user.save(update_fields=['password'])
            request.session.pop('reset_phone', None)
            login(request, user, backend=AUTH_BACKEND)
            messages.success(request, tr(request, 'pw_changed'))
            return redirect('restaurants:cabinet')
    return render(request, 'accounts/password_reset_set.html')


def logout_view(request):
    logout(request)
    return redirect('/')
