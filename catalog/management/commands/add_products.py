from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Product, Category


class Command(BaseCommand):
    help = 'Очищает базу и загружает тестовые данные из фикстур'

    def handle(self, *args, **options):
        self.stdout.write("Очистка базы данных...")
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write("Загрузка тестовых данных...")
        call_command('loaddata', 'Category.json', app_label='catalog')
        call_command('loaddata', 'Product.json', app_label='catalog')

        self.stdout.write(self.style.SUCCESS("Тестовые данные успешно загружены!"))