from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import PhoneOTP, User


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
            'phone', 'full_name', 'password', 'is_active', 'is_staff',
            'is_superuser', 'groups', 'user_permissions',
        )


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User

    list_display = ('phone', 'full_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('phone', 'full_name')
    ordering = ('phone',)
    filter_horizontal = ('groups', 'user_permissions')

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Личное', {'fields': ('full_name',)}),
        ('Права', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Даты', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'full_name', 'password1', 'password2'),
        }),
    )


@admin.register(PhoneOTP)
class PhoneOTPAdmin(admin.ModelAdmin):
    list_display = ('phone', 'code', 'is_used', 'attempts', 'created_at')
    list_filter = ('is_used',)
    search_fields = ('phone',)
