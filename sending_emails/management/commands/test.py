import smtplib
from datetime import datetime, timedelta
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.core.mail import send_mail
from django.core.cache import cache
from sending_emails.models import Mailing, MailingAttempt
from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        zone = pytz.timezone(settings.TIME_ZONE)
        today = datetime.now(zone)
        mailings = Mailing.objects.filter(mailing_status__in=['created', 'executing'])

        for mailing in mailings:
            print("-------")
            # Завершить отправку если заблокировано(снят флаг)
            if not mailing.is_active:
                continue
            # Завершить отправку по достижению даты окончания рассылки и назначить статус - завершен
            if today >= mailing.end_time:
                mailing.mailing_status = 'finished'
                mailing.save()
                continue
            # Завершить отправку - её время еще не пришло
            if today < mailing.start_time:
                continue
            # Назначаем следующее время для отправки
            if not mailing.next_time_mailing:
                mailing.next_time_mailing = today
                mailing.save()
            # Проверить, нужно ли отправить сообщение в текущий момент времени, с запасом в 10 секунд
            if mailing.next_time_mailing <= today <= (mailing.next_time_mailing + timedelta(seconds=10)):
                mailing.mailing_status = 'executing'
                mailing.save()
                clients = mailing.clients.all()
                try:
                    for client in clients:
                        server_response = send_mail(
                            subject=mailing.message.subject_message,
                            message=mailing.message.message,
                            from_email=settings.EMAIL_HOST_USER,
                            recipient_list=[client.email],
                        )
                    MailingAttempt.objects.create(status='successfully',
                                                  mail_response=server_response,
                                                  mailing=mailing, )
                except smtplib.SMTPException as e:
                    MailingAttempt.objects.create(status='not_successful',
                                                  mail_response=str(e),
                                                  mailing=mailing, )

                # Изменяем время следующей отправки сообщений
                if mailing.frequency == 'per_day':
                    mailing.next_time_mailing += timedelta(days=1)
                elif mailing.frequency == 'per_week':
                    mailing.next_time_mailing += timedelta(weeks=1)
                elif mailing.frequency == 'per_month':
                    mailing.next_time_mailing += timedelta(days=30)
                mailing.save()
