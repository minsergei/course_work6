from django.apps import AppConfig
from time import sleep


class SendingEmailsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sending_emails"

    def ready(self):
        from sending_emails.services import start_scheduler
        sleep(2)
        start_scheduler()
