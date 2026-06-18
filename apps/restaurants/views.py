import io

import qrcode
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import ensure_csrf_cookie

from apps.core.translations import resolve_lang
from apps.core.translations import t as translate
from apps.core.translations import tr

from .access import assignable_roles, can, can_manage, membership_for, perms_of
from .forms import TableForm
from .models import Membership, Restaurant, Table


def _get_restaurant(request, slug, perm=None):
    """Заведение текущего пользователя. `perm` — требуемая зона доступа (RBAC).

    Прячем и отсутствие доступа, и нехватку прав за 404 (не светим существование).
    Найденную роль кладём в `request.membership` для шелла и шаблонов.
    """
    restaurant = get_object_or_404(Restaurant, slug=slug)
    membership = membership_for(request.user, restaurant)
    if membership is None:
        raise Http404
    if perm is not None and not can(membership, perm):
        raise Http404
    request.membership = membership
    return restaurant


def _shell(request, restaurant, active):
    """Общий контекст для шелла кабинета (сайдбар, переключатель заведений)."""
    membership = getattr(request, 'membership', None) or membership_for(request.user, restaurant)
    role_label = translate(resolve_lang(request), f'role_{membership.role}') if membership else ''
    return {
        'restaurant': restaurant,
        'active': active,
        'membership': membership,
        'role_label': role_label,
        'perms': perms_of(membership),
        'venues': (
            request.user.memberships
            .select_related('restaurant')
            .filter(is_active=True)
        ),
    }


@login_required
def cabinet(request):
    """Список заведений пользователя. Если оно одно — сразу в дашборд."""
    memberships = (
        request.user.memberships
        .select_related('restaurant')
        .filter(is_active=True)
    )
    if memberships.count() == 1:
        return redirect('restaurants:dashboard', slug=memberships[0].restaurant.slug)
    return render(request, 'restaurants/cabinet.html', {'memberships': memberships})


@login_required
def dashboard(request, slug):
    restaurant = _get_restaurant(request, slug)
    from apps.menu.models import Dish
    from apps.orders.models import Order
    ctx = _shell(request, restaurant, 'dashboard')
    ctx['tables_count'] = restaurant.tables.count()
    ctx['dishes_count'] = Dish.objects.filter(category__restaurant=restaurant).count()
    ctx['active_orders'] = restaurant.orders.filter(status__in=Order.FLOW).count()
    return render(request, 'cabinet/dashboard.html', ctx)


@login_required
def tables(request, slug):
    restaurant = _get_restaurant(request, slug, perm='tables')
    if request.method == 'POST':
        form = TableForm(request.POST)
        if form.is_valid():
            table = form.save(commit=False)
            table.restaurant = restaurant
            table.save()
            return redirect('restaurants:tables', slug=slug)
    else:
        form = TableForm()
    ctx = _shell(request, restaurant, 'tables')
    ctx['tables'] = restaurant.tables.all()
    ctx['form'] = form
    return render(request, 'cabinet/tables.html', ctx)


@login_required
def table_edit(request, slug, pk):
    restaurant = _get_restaurant(request, slug, perm='tables')
    table = get_object_or_404(Table, pk=pk, restaurant=restaurant)
    if request.method == 'POST':
        form = TableForm(request.POST, instance=table)
        if form.is_valid():
            form.save()
            return redirect('restaurants:tables', slug=slug)
    else:
        form = TableForm(instance=table)
    ctx = _shell(request, restaurant, 'tables')
    ctx['tables'] = restaurant.tables.all()
    ctx['form'] = form
    ctx['edit_table'] = table
    return render(request, 'cabinet/tables.html', ctx)


@login_required
def table_delete(request, slug, pk):
    restaurant = _get_restaurant(request, slug, perm='tables')
    table = get_object_or_404(Table, pk=pk, restaurant=restaurant)
    if request.method == 'POST':
        table.delete()
    return redirect('restaurants:tables', slug=slug)


@login_required
def table_qr_png(request, slug, pk):
    restaurant = _get_restaurant(request, slug, perm='tables')
    table = get_object_or_404(Table, pk=pk, restaurant=restaurant)
    url = request.build_absolute_uri(
        reverse('restaurants:guest_menu', args=[table.qr_token])
    )
    img = qrcode.make(url, box_size=10, border=2)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return HttpResponse(buf.getvalue(), content_type='image/png')


@login_required
def qr_sheet(request, slug):
    restaurant = _get_restaurant(request, slug, perm='tables')
    ctx = _shell(request, restaurant, 'qr')
    ctx['tables'] = restaurant.tables.all()
    return render(request, 'cabinet/qr_sheet.html', ctx)


# --- сотрудники --------------------------------------------------------------

@login_required
def staff(request, slug):
    """Список сотрудников + приглашение по телефону (доступ — зона staff)."""
    from apps.accounts.models import User, normalize_phone
    from django.contrib import messages

    restaurant = _get_restaurant(request, slug, perm='staff')
    actor = request.membership
    allowed = assignable_roles(actor)
    allowed_values = {r.value for r in allowed}

    if request.method == 'POST':
        phone = normalize_phone(request.POST.get('phone', ''))
        full_name = request.POST.get('full_name', '').strip()
        role = request.POST.get('role', '')
        if not phone or len(phone) < 9:
            messages.error(request, tr(request, 'staff_err_phone'))
        elif role not in allowed_values:
            messages.error(request, tr(request, 'staff_err_role'))
        else:
            user, created = User.objects.get_or_create(
                phone=phone, defaults={'full_name': full_name},
            )
            if created:
                user.set_unusable_password()
                user.save()
            elif full_name and not user.full_name:
                user.full_name = full_name
                user.save(update_fields=['full_name'])
            membership, m_created = Membership.objects.get_or_create(
                user=user, restaurant=restaurant, defaults={'role': role},
            )
            if not m_created:
                messages.error(request, tr(request, 'staff_err_exists'))
            else:
                messages.success(request, tr(request, 'staff_added'))
        return redirect('restaurants:staff', slug=slug)

    lang = resolve_lang(request)
    members = (
        restaurant.memberships
        .select_related('user')
        .order_by('-is_active', 'role', 'created_at')
    )
    rows = [
        {
            'm': m,
            'role_label': translate(lang, f'role_{m.role}'),
            'can_manage': can_manage(actor, m),
            'is_self': m.pk == actor.pk,
        }
        for m in members
    ]
    ctx = _shell(request, restaurant, 'staff')
    ctx['rows'] = rows
    ctx['assignable'] = [(r.value, translate(lang, f'role_{r.value}')) for r in allowed]
    return render(request, 'cabinet/staff.html', ctx)


@login_required
def staff_role(request, slug, pk):
    """Сменить роль сотрудника (только на роль из допустимых актору)."""
    restaurant = _get_restaurant(request, slug, perm='staff')
    target = get_object_or_404(Membership, pk=pk, restaurant=restaurant)
    if request.method == 'POST' and can_manage(request.membership, target):
        role = request.POST.get('role', '')
        if role in {r.value for r in assignable_roles(request.membership)}:
            target.role = role
            target.save(update_fields=['role'])
    return redirect('restaurants:staff', slug=slug)


@login_required
def staff_remove(request, slug, pk):
    """Убрать сотрудника из заведения (деактивировать membership)."""
    restaurant = _get_restaurant(request, slug, perm='staff')
    target = get_object_or_404(Membership, pk=pk, restaurant=restaurant)
    if request.method == 'POST' and can_manage(request.membership, target):
        target.delete()
    return redirect('restaurants:staff', slug=slug)


def _money(value):
    """Целое в сумах → «38 000» (разделитель — неразрывный пробел)."""
    return f'{value:,}'.replace(',', ' ')


@ensure_csrf_cookie
def guest_menu(request, qr_token):
    """Публичное меню стола: гость смотрит и собирает корзину (без регистрации)."""
    from apps.core.translations import resolve_lang

    table = get_object_or_404(
        Table.objects.select_related('restaurant'),
        qr_token=qr_token, is_active=True,
    )
    restaurant = table.restaurant
    lang = resolve_lang(request)

    categories = (
        restaurant.categories
        .filter(is_active=True)
        .prefetch_related('dishes__variants')
    )
    menu = []
    for cat in categories:
        dishes = []
        for d in cat.dishes.all():
            variants = [
                {'id': v.pk, 'name': v.name(lang), 'price': v.price, 'price_display': _money(v.price)}
                for v in d.variants.all()
            ]
            if not variants:
                continue
            dishes.append({
                'id': d.pk,
                'name': d.name(lang),
                'description': getattr(d, f'description_{lang}', '') or d.description_ru,
                'photo': d.photo,
                'weight': d.weight,
                'available': d.is_available,
                'variants': variants,
                'multi': len(variants) > 1,
            })
        if dishes:
            menu.append({'name': cat.name(lang), 'dishes': dishes})

    return render(request, 'public/menu.html', {
        'table': table,
        'restaurant': restaurant,
        'menu': menu,
    })
