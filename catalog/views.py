from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View

from .forms import ProductForm
from .models import Product


class HomeView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'pk'


class ContactsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'contacts.html')

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        response_text = (
            f"Пользователь: {name}\n"
            f"Телефон: {phone}\n"
            f"Сообщение: {message if message else 'Сообщение не указано'}"
        )
        return HttpResponse(response_text, content_type='text/plain; charset=utf-8')


class ProductCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')
    success_message = "Продукт успешно создан!"
    template_name = 'catalog/product_form.html'
    login_url = reverse_lazy('users:login')  # URL для перенаправления неавторизованных

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме')
        return super().form_invalid(form)


class ProductUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')
    success_message = "Продукт успешно обновлён!"
    template_name = 'catalog/product_form.html'
    login_url = reverse_lazy('users:login')

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме')
        return super().form_invalid(form)

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:home')
    template_name = 'catalog/product_confirm_delete.html'
    login_url = reverse_lazy('users:login')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Продукт успешно удалён!")
        return super().delete(request, *args, **kwargs)