from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render

from apps.core.translations import tr
from apps.restaurants.models import Membership, Restaurant
from apps.restaurants.utils import unique_slug

from .models import User, normalize_phone
from .services import issue_otp, verify_otp

AUTH_BACKEND = 'django.contrib.auth.backends.ModelBackend'


def register(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        rtype = request.POST.get('type', '').strip() or Restaurant.Type.RESTAURANT
        city = request.POST.get('city', '').strip()
        phone = request.POST.get('phone', '').strip()
        if not name or not phone:
            messages.error(request, tr(request, 'err_required'))
        else:
            request.session['reg_data'] = {'name': name, 'type': rtype, 'city': city, 'phone': phone}
            request.session['otp_phone'] = normalize_phone(phone)
            request.session['otp_mode'] = 'register'
            issue_otp(phone)
            messages.success(request, tr(request, 'msg_code_sent'))
            return redirect('accounts:verify')
    return render(request, 'accounts/register.html')


def login_view(request):
    if request.method == 'POST':
        phone = request.POST.get('phone', '').strip()
        nphone = normalize_phone(phone)
        if not User.objects.filter(phone=nphone).exists():
            messages.error(request, tr(request, 'err_no_user'))
        else:
            request.session['otp_phone'] = nphone
            request.session['otp_mode'] = 'login'
            issue_otp(phone)
            messages.success(request, tr(request, 'msg_code_sent'))
            return redirect('accounts:verify')
    return render(request, 'accounts/login.html')


def verify(request):
    phone = request.session.get('otp_phone')
    mode = request.session.get('otp_mode')
    if not phone or not mode:
        return redirect('accounts:login')

    if request.method == 'POST':
        code = request.POST.get('code', '').strip()
        if verify_otp(phone, code):
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

        messages.error(request, tr(request, 'err_invalid_code'))

    return render(request, 'accounts/verify.html', {'phone': phone})


def logout_view(request):
    logout(request)
    return redirect('/')
