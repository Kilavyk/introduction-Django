from datetime import date

from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Наименование",
        help_text="Введите наименование категории"
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Введите описание категории",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Наименование",
        help_text="Введите наименование товара"
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Введите описание товара",
        blank=True,
        null=True
    )
    photo = models.ImageField(
        upload_to="catalog/photo",
        blank=True,
        null=True,
        verbose_name="Фото",
        help_text="Загрузите фото продукта"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        help_text="Выберите категорию",
        blank=True,
        null=True
    )
    purchase_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена за покупку",
        help_text="Введите цену за покупку"
    )
    created_at = models.DateField(
        blank=True,
        null=True,
        default=date.today,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата последнего изменения"
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name", "category", "purchase_price"]

    def __str__(self):
        return self.name
