from django import forms

from .models import Restaurant, Table


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ('name', 'seats')


class RestaurantForm(forms.ModelForm):
    """Профиль заведения (Настройки). Slug не меняем — он завязан на URL."""

    class Meta:
        model = Restaurant
        fields = (
            'name', 'type', 'city', 'phone', 'logo',
            'description_ru', 'description_uz', 'description_en',
        )
