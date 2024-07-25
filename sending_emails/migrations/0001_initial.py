# Generated by Django 4.2 on 2024-07-23 21:45

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Clients",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="Почта"
                    ),
                ),
                ("fio", models.CharField(max_length=50, verbose_name="ФИО")),
                ("comment", models.TextField(blank=True, verbose_name="Коммент")),
            ],
            options={
                "verbose_name": "Клиент",
                "verbose_name_plural": "Клиенты",
            },
        ),
        migrations.CreateModel(
            name="MailingAttempt",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "last_attempt",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="дата и время последней попытки"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("successfully", "успешно"),
                            ("not_successful", "не успешно"),
                        ],
                        default=None,
                        verbose_name="статус попытки",
                    ),
                ),
                (
                    "mail_response",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        verbose_name="ответ почтового сервера",
                    ),
                ),
            ],
            options={
                "verbose_name": "Попытка рассылки",
                "verbose_name_plural": "Попытки рассылок",
                "permissions": [("change_is_active", "Может отключать рассылки.")],
            },
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "subject_massage",
                    models.CharField(max_length=80, verbose_name="Тема письма"),
                ),
                ("massage", models.TextField(verbose_name="Текст письма")),
            ],
            options={
                "verbose_name": "Сообщение",
                "verbose_name_plural": "Сообщения",
                "permissions": [
                    ("view_mailing", "Может просматривать любые рассылки.")
                ],
            },
        ),
        migrations.CreateModel(
            name="Mailing",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "start_time",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="Начало рассылки",
                    ),
                ),
                (
                    "end_time",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Конец рассылки"
                    ),
                ),
                (
                    "next_day",
                    models.DateTimeField(
                        blank=True,
                        null=True,
                        verbose_name="Следующая отправка рассылки",
                    ),
                ),
                (
                    "frequency",
                    models.CharField(
                        choices=[
                            ("per_day", "раз в день"),
                            ("per_week", "раз в неделю"),
                            ("per_month", "раз в месяц"),
                        ],
                        default="per_day",
                        max_length=50,
                        verbose_name="периодичность",
                    ),
                ),
                (
                    "mailing_status",
                    models.CharField(
                        choices=[
                            ("created", "создана"),
                            ("executing", "запущена"),
                            ("finished", "закончена успешно"),
                            ("error", "законечена с ошибками"),
                        ],
                        default="created",
                        max_length=80,
                        verbose_name="статус рассылки",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True, verbose_name="Блокировка Рассылки"
                    ),
                ),
                (
                    "clients",
                    models.ManyToManyField(
                        related_name="mailing",
                        to="sending_emails.clients",
                        verbose_name="Клиенты для рассылки",
                    ),
                ),
                (
                    "massage",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="sending_emails.message",
                        verbose_name="Cообщение",
                    ),
                ),
            ],
            options={
                "verbose_name": "Рассылка",
                "verbose_name_plural": "Рассылки",
            },
        ),
    ]