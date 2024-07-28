from django.urls import path
from users.apps import UsersConfig
from django.contrib.auth.views import LogoutView

from users.views import RegisterView, email_verification, LoginView, PasswordReset, UserListView, blocking_user

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name='users/login.html'), name='login'),
    path("logout/", LogoutView.as_view(), name='logout'),
    path("register/", RegisterView.as_view(), name='register'),
    path("email-confirm/<str:token>/", email_verification, name='email-confirm'),
    path("reset_password/", PasswordReset.as_view(), name='reset_password'),
    path('users_list/', UserListView.as_view(), name='users_list'),
    path('blocking_user/<int:pk>/', blocking_user, name='blocking_user'),
]
