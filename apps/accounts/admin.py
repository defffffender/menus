import calendar
from datetime import date

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils import timezone
from django.utils.html import format_html
from unfold.admin import ModelAdmin as UnfoldModelAdmin

from .models import Lead, PhoneOTP, User


def _add_months(d, months):
    """Прибавить календарные месяцы к дате (с поправкой на длину месяца)."""
    m = d.month - 1 + months
    y = d.year + m // 12
    m = m % 12 + 1
    return date(y, m, min(d.day, calendar.monthrange(y, m)[1]))


class SubscriptionStatusFilter(admin.SimpleListFilter):
    title = 'Статус подписки'
    parameter_name = 'sub_status'

    def lookups(self, request, model_admin):
        return [
            ('active', 'Активна'),
            ('expired', 'Истекла'),
            ('suspended', 'Приостановлена'),
            ('unlimited', 'Без срока'),
        ]

    def queryset(self, request, qs):
        today = timezone.localdate()
        v = self.value()
        if v == 'suspended':
            return qs.filter(subscription_suspended=True)
        if v == 'unlimited':
            return qs.filter(subscription_suspended=False, subscription_until__isnull=True)
        if v == 'active':
            return qs.filter(subscription_suspended=False, subscription_until__gte=today)
        if v == 'expired':
            return qs.filter(subscription_suspended=False, subscription_until__lt=today)
        return qs


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone', 'full_name')

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Пароли не совпадают')
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label='Пароль')

    class Meta:
        model = User
        fields = (
            'phone', 'full_name', 'plan', 'subscription_until', 'subscription_suspended',
            'is_agent', 'password', 'is_active', 'is_staff',
            'is_superuser', 'groups', 'user_permissions',
        )


@admin.register(User)
class UserAdmin(BaseUserAdmin, UnfoldModelAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User

    list_display = ('phone', 'full_name', 'plan', 'subscription_badge', 'is_agent', 'is_active')
    list_filter = (SubscriptionStatusFilter, 'is_agent', 'plan', 'subscription_suspended', 'is_staff', 'is_active')
    list_editable = ('plan', 'is_agent')
    search_fields = ('phone', 'full_name')
    ordering = ('phone',)
    filter_horizontal = ('groups', 'user_permissions')
    actions = ('extend_1m', 'extend_3m', 'extend_12m', 'suspend_subscription', 'resume_subscription')

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Личное', {'fields': ('full_name',)}),
        ('Тариф и подписка', {'fields': ('plan', 'subscription_until', 'subscription_suspended')}),
        ('Роль', {'fields': ('is_agent',)}),
        ('Права', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Даты', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'full_name', 'password1', 'password2'),
        }),
    )

    @admin.display(description='Подписка')
    def subscription_badge(self, obj):
        s = obj.subscription_status
        colors = {'active': '#3E5C4A', 'expired': '#C0392B', 'suspended': '#B7791F', 'unlimited': '#9A8C78'}
        labels = {'active': 'Активна', 'expired': 'Истекла', 'suspended': 'Приостановлена', 'unlimited': 'Без срока'}
        text = labels[s]
        if obj.subscription_until and s in ('active', 'expired'):
            text += f' · до {obj.subscription_until:%d.%m.%Y}'
        return format_html('<b style="color:{}">{}</b>', colors[s], text)

    def _extend(self, request, queryset, months):
        today = timezone.localdate()
        n = 0
        for u in queryset:
            base = u.subscription_until if (u.subscription_until and u.subscription_until > today) else today
            u.subscription_until = _add_months(base, months)
            u.subscription_suspended = False  # продление снимает приостановку
            u.save(update_fields=['subscription_until', 'subscription_suspended'])
            n += 1
        self.message_user(request, f'Подписка продлена на {months} мес. у {n} польз.')

    @admin.action(description='Продлить подписку на 1 месяц')
    def extend_1m(self, request, queryset):
        self._extend(request, queryset, 1)

    @admin.action(description='Продлить подписку на 3 месяца')
    def extend_3m(self, request, queryset):
        self._extend(request, queryset, 3)

    @admin.action(description='Продлить подписку на 12 месяцев')
    def extend_12m(self, request, queryset):
        self._extend(request, queryset, 12)

    @admin.action(description='Приостановить подписку')
    def suspend_subscription(self, request, queryset):
        n = queryset.update(subscription_suspended=True)
        self.message_user(request, f'Приостановлено: {n}')

    @admin.action(description='Возобновить подписку')
    def resume_subscription(self, request, queryset):
        n = queryset.update(subscription_suspended=False)
        self.message_user(request, f'Возобновлено: {n}')


@admin.register(Lead)
class LeadAdmin(UnfoldModelAdmin):
    list_display = ('venue_name', 'venue_type', 'phone', 'city', 'is_processed', 'created_at')
    list_filter = ('is_processed', 'venue_type', 'created_at')
    list_editable = ('is_processed',)
    search_fields = ('venue_name', 'full_name', 'phone')
    readonly_fields = ('created_at',)


@admin.register(PhoneOTP)
class PhoneOTPAdmin(UnfoldModelAdmin):
    list_display = ('phone', 'code', 'is_used', 'attempts', 'created_at')
    list_filter = ('is_used',)
    search_fields = ('phone',)
