from django import forms

from .models import Category, Dish


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name_ru', 'name_uz', 'name_en')


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = (
            'category',
            'name_ru', 'name_uz', 'name_en',
            'description_ru', 'description_uz', 'description_en',
            'photo', 'weight', 'spiciness', 'prep_time',
            'is_available',
        )

    def __init__(self, *args, restaurant=None, **kwargs):
        super().__init__(*args, **kwargs)
        if restaurant is not None:
            self.fields['category'].queryset = restaurant.categories.all()
