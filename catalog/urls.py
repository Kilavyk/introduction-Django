from django.urls import path
from django.views.decorators.cache import cache_page

from . import views
from catalog.apps import CatalogConfig
from catalog.views import (ContactsView, HomeView, ProductCreateView, ProductDeleteView, ProductDetailView,
                           ProductUpdateView, CategoryProductsView)

app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('product_detail/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product_detail'),  # 1 минута кеша
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('product/unpublish/<int:pk>/', views.unpublish_product, name='unpublish_product'),
    path('product/publish/<int:pk>/', views.publish_product, name='publish_product'),
    path('category/<str:category_name>/', CategoryProductsView.as_view(), name='category_products'),
]