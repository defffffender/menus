"""Агентский кабинет: агент подключает заведения — заводит им аккаунт
(телефон + пароль), и заведение получает доступ в свой личный кабинет.

Создавать заведения могут только агенты и суперпользователь.
"""
from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from apps.core.translations import tr
from apps.restaurants.models import Membership, Restaurant
from apps.restaurants.utils import unique_slug

from .models import User, is_valid_uz_phone, normalize_phone
from .views import _password_error


def agent_required(view):
    """Доступ только агентам и суперпользователю."""
    @wraps(view)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_agent_user:
            raise Http404
        return view(request, *args, **kwargs)
    return wrapper


@agent_required
def dashboard(request):
    """Список заведений, подключённых этим агентом."""
    qs = Restaurant.objects.select_related('owner').order_by('-created_at')
    if not request.user.is_superuser:
        qs = qs.filter(registered_by=request.user)
    return render(request, 'agent/dashboard.html', {
        'venues': qs,
        'venues_count': qs.count(),
    })


@agent_required
def register_venue(request):
    """Подключить заведение: создать аккаунт владельцу (телефон+пароль) и заведение."""
    values = {}
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        rtype = request.POST.get('type', '').strip() or Restaurant.Type.RESTAURANT
        city = request.POST.get('city', '').strip()
        full_name = request.POST.get('full_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        pw = request.POST.get('password', '')
        pw2 = request.POST.get('password2', '')
        nphone = normalize_phone(phone)
        values = {'name': name, 'type': rtype, 'city': city, 'full_name': full_name, 'phone': phone}

        pw_err = _password_error(request, pw, pw2, phone)
        if not name or not phone:
            messages.error(request, tr(request, 'err_required'))
        elif not is_valid_uz_phone(phone):
            messages.error(request, tr(request, 'err_phone_uz'))
        elif User.objects.filter(phone=nphone).exists():
            messages.error(request, tr(request, 'agent_phone_taken'))
        elif pw_err:
            messages.error(request, pw_err)
        else:
            owner = User.objects.create_user(phone=nphone, password=pw, full_name=full_name)
            restaurant = Restaurant.objects.create(
                owner=owner,
                registered_by=request.user,
                name=name,
                slug=unique_slug(name),
                type=rtype,
                city=city,
                phone=nphone,
            )
            Membership.objects.create(
                user=owner, restaurant=restaurant, role=Membership.Role.OWNER,
            )
            messages.success(request, f"{tr(request, 'agent_created')}: {name} · {nphone}")
            return redirect('accounts:agent_dashboard')
    return render(request, 'agent/register_venue.html', {'values': values})


@agent_required
def reset_password(request, pk):
    """Сбросить пароль владельца подключённого заведения (на случай онбординга)."""
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if not request.user.is_superuser and restaurant.registered_by_id != request.user.id:
        raise Http404
    if request.method == 'POST':
        pw = request.POST.get('password', '')
        pw2 = request.POST.get('password2', '')
        err = _password_error(request, pw, pw2, restaurant.owner.phone)
        if err:
            messages.error(request, err)
        else:
            owner = restaurant.owner
            owner.set_password(pw)
            owner.save(update_fields=['password'])
            messages.success(request, tr(request, 'agent_pw_reset_ok'))
            return redirect('accounts:agent_dashboard')
    return render(request, 'agent/reset_password.html', {'restaurant': restaurant})
