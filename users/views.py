from django.views.generic import CreateView
from users.forms import UserRegisterForm
from users.models import User
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
import secrets
from config.settings import EMAIL_HOST_USER
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.forms import PasswordResetForm


class LoginView(BaseLoginView):
    template_name = 'users/login.html'


class PasswordReset(PasswordResetView):
    model = User
    form_class = PasswordResetForm
    template_name = 'users/reset_password.html'

    def form_valid(self, form):
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            if user:
                password = User.objects.make_random_password(12)
                user.set_password(password)
                user.save()
                send_mail(
                    subject="Восстановление пароля",
                    message=f"Ваш новый пароль: {password}",
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[user.email],
                )
            return redirect(reverse("users:login"))


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject='Подтверждение почты',
            message=f"Перейди по ссылке для подтверждения почты {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))
