from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from catalog.models import Product

class Command(BaseCommand):
    help = "Создает группу 'Модератор продуктов' и назначает права"

    def handle(self, *args, **kwargs):
        # Получаем разрешения
        unpublish_perm = Permission.objects.get(codename="can_unpublish_product")
        delete_perm = Permission.objects.get(codename="delete_product")

        # Создаем группу
        group, created = Group.objects.get_or_create(name="Модератор продуктов")
        group.permissions.add(unpublish_perm, delete_perm)
        group.save()

        self.stdout.write(self.style.SUCCESS("Группа 'Модератор продуктов' создана!"))
