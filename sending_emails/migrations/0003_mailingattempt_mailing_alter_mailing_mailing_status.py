# Generated by Django 4.2 on 2024-07-25 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        (
            "sending_emails",
            "0002_remove_mailing_next_day_mailing_next_time_mailing_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="mailingattempt",
            name="mailing",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="sending_emails.mailing",
                verbose_name="Рассылка",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="mailing",
            name="mailing_status",
            field=models.CharField(
                choices=[
                    ("created", "создана"),
                    ("executing", "запущена"),
                    ("finished", "закончена успешно"),
                ],
                default="created",
                max_length=80,
                verbose_name="статус рассылки",
            ),
        ),
    ]
