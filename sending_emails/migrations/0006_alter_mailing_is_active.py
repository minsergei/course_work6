# Generated by Django 4.2 on 2024-07-25 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sending_emails", "0005_alter_mailingattempt_mail_response"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailing",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="Рассылка разрешена"),
        ),
    ]
