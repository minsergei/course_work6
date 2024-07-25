import smtplib
from django.core.mail import send_mail
from django.core.management import BaseCommand
from sending_emails.models import Mailing, MailingAttempt
from config import settings


class Command(BaseCommand):

    def handle(self, *args, **options):
        """  Функция отправки письма из терминала с проверкой на ошибку в почтовом адресе """
        mailings = Mailing.objects.filter(mailing_status='executing')
        for mailing in mailings:
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
                                   mailing=mailing,)
            except smtplib.SMTPException as e:
                MailingAttempt.objects.create(status='not_successful',
                                   mail_response=str(e),
                                   mailing=mailing,)
