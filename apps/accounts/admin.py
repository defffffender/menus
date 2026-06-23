from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from unfold.admin import ModelAdmin as UnfoldModelAdmin

from .models import Lead, PhoneOTP, User


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
            'phone', 'full_name', 'plan', 'is_agent', 'password', 'is_active', 'is_staff',
            'is_superuser', 'groups', 'user_permissions',
        )


@admin.register(User)
class UserAdmin(BaseUserAdmin, UnfoldModelAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User

    list_display = ('phone', 'full_name', 'plan', 'is_agent', 'is_staff', 'is_active')
    list_filter = ('is_agent', 'plan', 'is_staff', 'is_superuser', 'is_active')
    list_editable = ('plan', 'is_agent')
    search_fields = ('phone', 'full_name')
    ordering = ('phone',)
    filter_horizontal = ('groups', 'user_permissions')

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Личное', {'fields': ('full_name',)}),
        ('Роль и тариф', {'fields': ('is_agent', 'plan')}),
        ('Права', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Даты', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'full_name', 'password1', 'password2'),
        }),
    )


@admin.register(Lead)
class LeadAdmin(UnfoldModelAdmin):
    list_display = ('venue_name', 'full_name', 'phone', 'city', 'is_processed', 'created_at')
    list_filter = ('is_processed', 'created_at')
    list_editable = ('is_processed',)
    search_fields = ('venue_name', 'full_name', 'phone')
    readonly_fields = ('created_at',)


@admin.register(PhoneOTP)
class PhoneOTPAdmin(UnfoldModelAdmin):
    list_display = ('phone', 'code', 'is_used', 'attempts', 'created_at')
    list_filter = ('is_used',)
    search_fields = ('phone',)
