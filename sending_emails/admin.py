from django.contrib import admin
from sending_emails.models import Clients, Message, Mailing, MailingAttempt


@admin.register(Clients)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "fio",
        "comment",
    )
    list_filter = ("fio",)
    search_fields = ("fio",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "subject_message",
        "message",
    )


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "start_time",
        "end_time",
        "next_time_mailing",
        "frequency",
        "mailing_status",
        "message",
        "is_active",
    )
    list_filter = ("mailing_status", "is_active",)


@admin.register(MailingAttempt)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "last_attempt",
        "status",
        "mail_response",
        "mailing",
    )
