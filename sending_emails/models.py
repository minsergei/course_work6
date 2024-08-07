from django.utils import timezone
from django.db import models

from users.models import User


class Clients(models.Model):
    email = models.EmailField(unique=True, verbose_name='Почта')
    fio = models.CharField(max_length=50, verbose_name='ФИО')
    comment = models.TextField(blank=True, verbose_name='Коммент')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Владелец', null=True, blank=True)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.fio}: {self.email} - {self.comment}'


class Message(models.Model):
    subject_message = models.CharField(max_length=80, verbose_name='Тема письма')
    message = models.TextField(verbose_name='Текст письма')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Владелец', null=True, blank=True)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        permissions = [
            ('view_mailing', 'Может просматривать любые рассылки.')]

    def __str__(self):
        return f'{self.subject_message} - {self.message}'


class Mailing(models.Model):
    period_variants = (
        ('per_day', 'раз в день'),
        ('per_week', 'раз в неделю'),
        ('per_month', 'раз в месяц')
    )

    status_variants = (
        ('created', 'создана'),
        ('executing', 'запущена'),
        ('finished', 'закончена успешно'),
    )

    start_time = models.DateTimeField(default=timezone.now, verbose_name='Начало рассылки', help_text="Формат DD.MM.YYYY HH:MM:SS",)
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='Конец рассылки', help_text="Формат DD.MM.YYYY HH:MM:SS",)
    next_time_mailing = models.DateTimeField(null=True, blank=True, verbose_name='Следующее время рассылки', help_text="Формат DD.MM.YYYY HH:MM:SS",)
    frequency = models.CharField(max_length=50, choices=period_variants, default='per_day',
                                 verbose_name='периодичность')
    mailing_status = models.CharField(max_length=80, choices=status_variants, default='created',
                                      verbose_name='статус рассылки')
    clients = models.ManyToManyField(Clients, related_name='mailing', verbose_name='Клиенты для рассылки')
    message = models.ForeignKey(Message, verbose_name='Cообщение', on_delete=models.CASCADE, blank=True, null=True)

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Владелец', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Рассылка разрешена')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [
            ('deactivate_mailing', 'Can deactivate mailing'),
        ]

    def __str__(self):
        return f'{self.start_time} - {self.end_time} - {self.frequency} - {self.mailing_status}'


class MailingAttempt(models.Model):
    status_variants = (
        ('successfully', 'успешно'),
        ('not_successful', 'не успешно'),
    )

    last_attempt = models.DateTimeField(auto_now_add=True, verbose_name='дата и время последней попытки')
    status = models.CharField(choices=status_variants, default=None, verbose_name='статус попытки')
    mail_response = models.CharField(max_length=100, verbose_name='ответ почтового сервера', blank=True, null=True)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name="Рассылка")

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылок'
        permissions = [
            ('change_is_active', 'Может отключать рассылки.'), ]

    def __str__(self):
        return f'{self.last_attempt} - {self.status} - {self.mail_response}'
