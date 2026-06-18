"""Права доступа по ролям (RBAC) для кабинета заведения.

Зоны доступа: menu (меню), tables (столы/QR), orders (заказы), staff (сотрудники).
Роли хранятся в `Membership.role` — матрица легко расширяется.
"""
from .models import Membership

Role = Membership.Role

# какие зоны доступны каждой роли
ROLE_PERMS = {
    Role.OWNER:         {'menu', 'tables', 'orders', 'staff'},
    Role.DIRECTOR:      {'menu', 'tables', 'orders', 'staff'},
    Role.ADMINISTRATOR: {'menu', 'tables', 'orders', 'staff'},  # сотрудники — частично (см. ранг)
    Role.MANAGER:       {'menu', 'tables', 'orders'},
    Role.WAITER:        {'orders'},
    Role.KITCHEN:       {'orders'},
}

# ранг для управления сотрудниками: можно назначать/трогать роли строго ниже своей
ROLE_RANK = {
    Role.OWNER: 5,
    Role.DIRECTOR: 4,
    Role.ADMINISTRATOR: 3,
    Role.MANAGER: 2,
    Role.WAITER: 1,
    Role.KITCHEN: 1,
}


def membership_for(user, restaurant):
    if not user.is_authenticated:
        return None
    return (
        Membership.objects
        .filter(user=user, restaurant=restaurant, is_active=True)
        .first()
    )


def can(membership, perm):
    return bool(membership) and perm in ROLE_PERMS.get(membership.role, set())


def perms_of(membership):
    return ROLE_PERMS.get(membership.role, set()) if membership else set()


def assignable_roles(membership):
    """Роли, которые этот сотрудник вправе назначать (строго ниже своего ранга)."""
    if not can(membership, 'staff'):
        return []
    my_rank = ROLE_RANK.get(membership.role, 0)
    return [r for r in Role if 0 < ROLE_RANK.get(r, 0) < my_rank]


def can_manage(actor, target):
    """Может ли actor менять/удалять membership target."""
    if not can(actor, 'staff') or actor.pk == target.pk:
        return False
    if target.role == Role.OWNER:
        return False
    return ROLE_RANK.get(actor.role, 0) > ROLE_RANK.get(target.role, 0)
