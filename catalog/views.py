from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View

from .forms import ProductForm
from .models import Product


class HomeView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user  # Добавляем пользователя в контекст
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'pk'
    login_url = reverse_lazy('users:login')


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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Автоматически назначаем владельца
        return super().form_valid(form)


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

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()

        # Проверяем, может ли пользователь отменять публикацию
        if request.POST.get("unpublish") and not request.user.has_perm("catalog.can_unpublish_product"):
            raise PermissionDenied("У вас нет прав на отмену публикации!")

        # Проверяем, является ли пользователь владельцем или администратором
        if not (product.owner == request.user or request.user.is_staff):
            raise PermissionDenied("Вы не можете редактировать этот продукт!")

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:home')
    template_name = 'catalog/product_confirm_delete.html'
    login_url = reverse_lazy('users:login')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Продукт успешно удалён!")
        return super().delete(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()

        # Является ли пользователь владельцем или администратором
        if not (product.owner == request.user or request.user.is_staff or request.user.has_perm(
                'catalog.can_delete_any_product')):
            raise PermissionDenied("Вы не можете удалить этот продукт!")

        return super().dispatch(request, *args, **kwargs)

@permission_required('catalog.can_unpublish_product')
def unpublish_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.status = 'draft'
    product.save()
    messages.success(request, 'Публикация продукта отменена')
    return redirect('catalog:product_detail', pk=pk)

@permission_required('catalog.can_unpublish_product')
def publish_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.status = 'published'
    product.save()
    messages.success(request, 'Продукт опубликован')
    return redirect('catalog:product_detail', pk=pk)
