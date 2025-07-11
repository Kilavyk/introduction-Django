from django import forms
from django.core.exceptions import ValidationError

from .models import Product

FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
]


def validate_forbidden_words(value):
    value_lower = value.lower()
    for word in FORBIDDEN_WORDS:
        if word in value_lower:
            raise ValidationError(
                f'Использование слова "{word}" запрещено в названиях и описаниях продуктов'
            )


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Если пользователь не модератор - скрываем поле статуса
        if not user or not user.has_perm('catalog.can_unpublish_product'):
            self.fields.pop('status', None)

        # стилизация для всех полей
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

            # стилизация для чекбокса
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
                self.fields[field_name].label_attrs = {'class': 'form-check-label'}

            # placeholder для текстовых полей
            if isinstance(field.widget, (forms.TextInput, forms.Textarea)):
                field.widget.attrs['placeholder'] = field.help_text

            # стилизация для поля цены
            if field_name == 'purchase_price':
                field.widget.attrs['step'] = '0.01'
                field.widget.attrs['placeholder'] = field.help_text

    def clean_name(self):
        name = self.cleaned_data['name']
        validate_forbidden_words(name)
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description', '')
        if description:
            validate_forbidden_words(description)
        return description

    def clean_purchase_price(self):
        price = self.cleaned_data.get('purchase_price')
        if price is not None and price <= 0:
            raise ValidationError("Цена продукта не может быть отрицательной")
        return price