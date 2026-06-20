from django import forms

from apps.core.images import downscale_field, validate_image_size

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

    def clean_logo(self):
        logo = self.cleaned_data.get('logo')
        validate_image_size(logo)
        return logo

    def save(self, commit=True):
        obj = super().save(commit=commit)
        if commit and 'logo' in self.changed_data and obj.logo:
            downscale_field(obj.logo, max_px=512)
            obj.save(update_fields=['logo'])
        return obj
