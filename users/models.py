from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Необходимо указать адрес электронной почты')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email', help_text='Введите почту')
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', blank=True, null=True, help_text='Загрузите аватарку')
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', blank=True, null=True, help_text='Введите номер телефона')
    country = models.CharField(max_length=100, verbose_name='Страна', blank=True, null=True, help_text='Введите страну проживания')

    USERNAME_FIELD = 'email'  # Используем email для авторизации
    REQUIRED_FIELDS = []  # Убираем username из обязательных полей

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
