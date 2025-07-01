# from django.urls import path
# from catalog.apps import CatalogConfig
# from catalog.views import home, product_detail
# from catalog.views import contacts
#
# app_name = CatalogConfig.name
#
# urlpatterns = [
#     path('', home, name='home'),  # корневой URL
#     path('contacts/', contacts, name='contacts'),  # URL для контактов
#     path('product_detail/<int:pk>/', product_detail, name='product_detail')
# ]

from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import HomeView, ProductDetailView, ContactsView

app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  # корневой URL
    path('contacts/', ContactsView.as_view(), name='contacts'),  # URL для контактов
    path('product_detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail')
]