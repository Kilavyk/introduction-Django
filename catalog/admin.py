from django.contrib import admin

from catalog.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Поля для отображения в списке
    search_fields = ('name',)  # Поля для поиска


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'purchase_price', 'category', 'created_at')  # Поля в списке
    list_filter = ('category', 'created_at',)  # Фильтрация по категории и дате создания
    search_fields = ('name', 'description')  # Поля для поиска

    list_editable = ('purchase_price', 'category')  # Возможность редактировать прямо из списка
    readonly_fields = ('created_at', 'updated_at',)  # Только для чтения
