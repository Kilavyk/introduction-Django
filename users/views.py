from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import FormView, RedirectView, TemplateView, UpdateView

from .forms import UserDeleteForm, UserLoginForm, UserProfileForm, UserRegisterForm
from .models import User


class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()

        # Отправка приветственного письма
        send_mail(
            'Добро пожаловать!',
            'Спасибо за регистрацию в нашем сервисе.',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

        messages.success(self.request, 'Вы успешно зарегистрированы!')
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('catalog:home')


class UserLogoutView(RedirectView):
    url = reverse_lazy('catalog:home')

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, 'Вы успешно вышли из системы')
        return super().get(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Профиль успешно обновлен')
        return super().form_valid(form)


class DeleteAccountView(LoginRequiredMixin, FormView):
    template_name = 'users/delete_account.html'
    form_class = UserDeleteForm
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        user = self.request.user
        logout(self.request)
        user.delete()
        messages.success(self.request, 'Ваш аккаунт был успешно удален')
        return super().form_valid(form)