from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  # Импортируем стандартный UserAdmin
from .models import User  # Импортируем нашу модель User

# Регистрируем модель User с кастомным админ-классом
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone', 'country', 'is_staff', 'is_active')  # Какие поля отображать
    list_filter = ('is_staff', 'is_superuser', 'is_active')  # Фильтры справа
    search_fields = ('email', 'first_name', 'last_name', 'phone')  # Поиск по этим полям
    ordering = ('email',)  # Сортировка по email

    # Настройка полей в форме редактирования пользователя
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'country', 'avatar')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Настройка полей при создании пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )