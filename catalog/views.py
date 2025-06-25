from itertools import product

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from catalog.models import Product


def home(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, 'home.html', context)

# def contacts(request):
#     return render(request, 'contacts.html')

def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Формируем ответ
        response_text = (
            f"Пользователь: {name}\n"
            f"Телефон: {phone}\n"
            f"Сообщение: {message if message else 'Сообщение не указано'}"
        )
        return HttpResponse(response_text, content_type='text/plain; charset=utf-8')

    return render(request, 'contacts.html')


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {"product": product}
    return render(request, 'product_detail.html', context)