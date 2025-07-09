from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm

from .models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')  # Переопределяем username как email
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class UserProfileForm(UserChangeForm):
    password = None  # Убираем поле смены пароля

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'country', 'avatar')


class UserDeleteForm(forms.Form):
    confirm = forms.BooleanField(
        label="Я подтверждаю удаление аккаунта",
        required=True
    )