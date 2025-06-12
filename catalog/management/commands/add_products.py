from django.core.management.base import BaseCommand
from catalog.models import Category, Product
from datetime import date


class Command(BaseCommand):
    help = 'Добавляет тестовые продукты в базу данных (с предварительной очисткой)'

    def handle(self, *args, **options):
        # Очищаем существующие данные
        self.stdout.write("Очистка старых данных...")
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Создаем тестовую категорию
        category, _ = Category.objects.get_or_create(
            name='Электроника',
            defaults={'description': 'Гаджеты и устройства'}
        )

        # Список тестовых продуктов
        products = [
            {
                'name': 'Смартфон X10',
                'description': 'Флагманский смартфон',
                'category': category,
                'purchase_price': 799.99,
                'created_at': date(2023, 1, 15)
            },
            {
                'name': 'Ноутбук Pro',
                'description': 'Мощный ноутбук',
                'category': category,
                'purchase_price': 1299.99,
                'created_at': date(2023, 2, 20)
            },
            {
                'name': 'Планшет Mini',
                'description': 'Компактный планшет',
                'category': category,
                'purchase_price': 399.99,
                'created_at': date(2023, 3, 10)
            },
        ]

        # Добавляем продукты
        for product_data in products:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults=product_data
            )

            if created:
                self.stdout.write(self.style.SUCCESS(
                    f'Успешно добавлен продукт: {product.name}'
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f'Продукт уже существует: {product.name}'
                ))

        self.stdout.write(self.style.SUCCESS(
            "Тестовые продукты успешно добавлены!"
        ))
