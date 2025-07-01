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
        super().__init__(*args, **kwargs)
        # Общая стилизация для всех полей
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

            # Специальная стилизация для чекбокса
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
                self.fields[field_name].label_attrs = {'class': 'form-check-label'}

            # Добавляем placeholder для текстовых полей
            if isinstance(field.widget, (forms.TextInput, forms.Textarea)):
                field.widget.attrs['placeholder'] = field.help_text or ''

            # Стилизация для поля цены
            if field_name == 'purchase_price':
                field.widget.attrs['step'] = '0.01'

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