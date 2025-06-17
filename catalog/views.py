from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, 'home.html')

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