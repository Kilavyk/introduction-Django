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

    def clean_name(self):
        name = self.cleaned_data['name']
        validate_forbidden_words(name)
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description', '')
        if description:  # проверяем только если описание не пустое
            validate_forbidden_words(description)
        return description