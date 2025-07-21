from django.core.cache import cache

from config.settings import CACHE_ENABLED
from .models import Category, Product


PRODUCTS_CACHE_TIMEOUT = 60  # 1 минута


def categories(request):
    return {
        'categories': Category.objects.all()
    }


def get_product_from_cache():
    """Получает список продуктов из кеша или БД"""
    key = "product_list"
    products = cache.get(key)
    if products is None:
        products = Product.objects.all()
        cache.set(key, products, PRODUCTS_CACHE_TIMEOUT)
    return products

# def get_product_from_cache():
#     """Получает данные о продуктах из кеша, если кеш пуст, получает данные из БД"""
#     if not CACHE_ENABLED:
#         return Product.objects.all()
#
#     key = "product_list"
#     products = cache.get(key)
#     if products is not None:
#         return products
#
#     products = Product.objects.all()
#     cache.set(key, products)
#     return products
