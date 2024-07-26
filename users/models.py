from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name="email", unique=True)
    avatar = models.ImageField(
        upload_to="media/users/",
        null=True,
        blank=True,
        verbose_name="Аватар",
        help_text="Укажите аватар",
    )
    telephone = models.CharField(
        max_length=35,
        verbose_name="телефон",
        help_text="Введите телефон",
        null=True,
        blank=True,
    )
    country = models.CharField(
        max_length=35,
        verbose_name="страна",
        help_text="Введите страну",
        null=True,
        blank=True,
    )
    token = models.CharField(
        max_length=50,
        verbose_name="токен",
        null=True,
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
