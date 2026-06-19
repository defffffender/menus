import io

import qrcode
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie

from apps.core.translations import resolve_lang
from apps.core.translations import t as translate
from apps.core.translations import tr

from .access import (
    assignable_roles,
    can,
    can_manage,
    membership_for,
    owns_any_venue,
    perms_of,
)
from .forms import RestaurantForm, TableForm
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
    venues = list(
        request.user.memberships
        .select_related('restaurant')
        .filter(is_active=True)
    )
    can_create = owns_any_venue(request.user)
    has_other = any(v.restaurant_id != restaurant.id for v in venues)
    return {
        'restaurant': restaurant,
        'active': active,
        'membership': membership,
        'role_label': role_label,
        'perms': perms_of(membership),
        'can_create_venue': can_create,
        # переключатель показываем только если есть куда переключиться
        'can_switch_venue': has_other or can_create,
        'venues': venues,
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
    return render(request, 'restaurants/cabinet.html', {
        'memberships': memberships,
        'can_create_venue': owns_any_venue(request.user),
    })


@login_required
def venue_create(request):
    """Добавить ещё одно заведение. Доступно ТОЛЬКО действующим владельцам:
    первое заведение создаётся при регистрации, сотрудники владельцами не становятся."""
    from .utils import unique_slug

    if not owns_any_venue(request.user):
        raise Http404

    at_limit = not request.user.can_add_venue

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        rtype = request.POST.get('type', '').strip() or Restaurant.Type.RESTAURANT
        city = request.POST.get('city', '').strip()
        if at_limit:
            messages.error(request, tr(request, 'plan_limit_venues'))
        elif not name:
            messages.error(request, tr(request, 'err_required'))
        else:
            restaurant = Restaurant.objects.create(
                owner=request.user, name=name, slug=unique_slug(name),
                type=rtype, city=city, phone=request.user.phone,
            )
            Membership.objects.create(
                user=request.user, restaurant=restaurant, role=Membership.Role.OWNER,
            )
            messages.success(request, tr(request, 'venue_created'))
            return redirect('restaurants:dashboard', slug=restaurant.slug)
    return render(request, 'cabinet/venue_form.html', {
        'venues': request.user.memberships.select_related('restaurant').filter(is_active=True),
        'at_limit': at_limit,
        'venue_limit': request.user.venue_limit,
        'venues_used': request.user.venues_used,
    })


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

def _staff_admin_venues(user):
    """Заведения, куда этот пользователь вправе привязывать сотрудников
    в любое (владелец/директор). Для них показываем выбор заведения."""
    Role = Membership.Role
    return list(
        Membership.objects
        .filter(user=user, is_active=True, role__in=[Role.OWNER, Role.DIRECTOR])
        .select_related('restaurant')
    )


@login_required
def staff(request, slug):
    """Список сотрудников + приглашение по телефону (доступ — зона staff).

    Владелец/директор может сразу привязать сотрудника к любому своему
    заведению, не переключаясь в его кабинет.
    """
    from apps.accounts.models import User, is_valid_uz_phone, normalize_phone

    restaurant = _get_restaurant(request, slug, perm='staff')
    actor = request.membership
    allowed = assignable_roles(actor)
    allowed_values = {r.value for r in allowed}

    # заведения, между которыми можно выбирать при приглашении
    admin_venues = _staff_admin_venues(request.user)
    show_venue_picker = (
        actor.role in (Membership.Role.OWNER, Membership.Role.DIRECTOR)
        and len(admin_venues) > 1
    )

    if request.method == 'POST':
        raw_phone = request.POST.get('phone', '')
        phone = normalize_phone(raw_phone)
        full_name = request.POST.get('full_name', '').strip()
        role = request.POST.get('role', '')

        # к каким заведениям привязываем. Мультивыбор — только для владельца/
        # директора с несколькими заведениями; иначе всегда текущее.
        if show_venue_picker:
            target_slugs = request.POST.getlist('venues') or []
        else:
            target_slugs = [slug]

        # резолвим цели и проверяем права на каждое
        targets = []  # (restaurant, role) валидные
        bad_perm = False
        bad_role = False
        for ts in target_slugs:
            t = Restaurant.objects.filter(slug=ts).first()
            tm = membership_for(request.user, t) if t else None
            if tm is None or tm.role not in (Membership.Role.OWNER, Membership.Role.DIRECTOR):
                bad_perm = True
                continue
            if role not in {r.value for r in assignable_roles(tm)}:
                bad_role = True
                continue
            targets.append(t)

        if not is_valid_uz_phone(raw_phone):
            messages.error(request, tr(request, 'err_phone_uz'))
        elif not target_slugs:
            messages.error(request, tr(request, 'staff_err_no_venue'))
        elif bad_perm:
            messages.error(request, tr(request, 'staff_err_venue'))
        elif bad_role or not targets:
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
            added = 0
            for t in targets:
                _, m_created = Membership.objects.get_or_create(
                    user=user, restaurant=t, defaults={'role': role},
                )
                added += 1 if m_created else 0
            if added:
                msg = tr(request, 'staff_added')
                if len(targets) > 1:
                    msg = f"{tr(request, 'staff_added_n')}: {added}"
                messages.success(request, msg)
            else:
                messages.error(request, tr(request, 'staff_err_exists'))
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
    ctx['show_venue_picker'] = show_venue_picker
    ctx['venue_choices'] = [m.restaurant for m in admin_venues] if show_venue_picker else []
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


# --- аналитика ---------------------------------------------------------------

@login_required
def analytics(request, slug):
    """Сводка по заказам: сегодня, неделя, топ блюд. Оплату не считаем —
    «выручка» = сумма незаотменённых заказов (что заказали)."""
    from apps.orders.models import Order, OrderItem

    restaurant = _get_restaurant(request, slug, perm='analytics')
    today = timezone.localdate()
    week_start = today - timezone.timedelta(days=6)

    def revenue(qs):
        return qs.aggregate(s=Sum(F('price') * F('quantity')))['s'] or 0

    # сегодня
    today_orders = restaurant.orders.filter(created_at__date=today).exclude(status=Order.Status.CANCELLED)
    today_count = today_orders.count()
    today_rev = revenue(OrderItem.objects.filter(order__in=today_orders))
    avg_check = today_rev // today_count if today_count else 0

    # неделя (7 дней)
    week_orders = restaurant.orders.filter(created_at__date__gte=week_start).exclude(status=Order.Status.CANCELLED)
    week_count = week_orders.count()
    week_rev = revenue(OrderItem.objects.filter(order__in=week_orders))

    # топ-5 блюд за неделю
    top = list(
        OrderItem.objects.filter(order__in=week_orders)
        .values('name')
        .annotate(qty=Sum('quantity'), rev=Sum(F('price') * F('quantity')))
        .order_by('-qty')[:5]
    )
    for t in top:
        t['rev_display'] = _money(t['rev'])

    ctx = _shell(request, restaurant, 'analytics')
    ctx.update({
        'active_now': restaurant.orders.filter(status__in=Order.FLOW).count(),
        'today_count': today_count,
        'today_rev': _money(today_rev),
        'avg_check': _money(avg_check),
        'week_count': week_count,
        'week_rev': _money(week_rev),
        'top': top,
    })
    return render(request, 'cabinet/analytics.html', ctx)


# --- настройки заведения -----------------------------------------------------

@login_required
def settings_view(request, slug):
    """Профиль заведения: название, тип, город, телефон, лого, описания (3 языка)."""
    restaurant = _get_restaurant(request, slug, perm='settings')
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            form.save()
            messages.success(request, tr(request, 'set_saved'))
            return redirect('restaurants:settings', slug=slug)
    else:
        form = RestaurantForm(instance=restaurant)
    from apps.menu.models import Dish
    owner = restaurant.owner
    plan_label_key = {'start': 'l_plan_start', 'business': 'l_plan_pro', 'network': 'l_plan_net'}.get(owner.plan, 'l_plan_start')
    ctx = _shell(request, restaurant, 'settings')
    ctx['form'] = form
    ctx['plan_label'] = translate(resolve_lang(request), plan_label_key)
    ctx['venue_limit'] = owner.venue_limit
    ctx['venues_used'] = owner.venues_used
    ctx['dish_limit'] = owner.dish_limit
    ctx['dishes_used'] = Dish.objects.filter(category__restaurant=restaurant).count()
    return render(request, 'cabinet/settings.html', ctx)


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
