# Generated by Django 5.1.1 on 2024-11-27 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0010_remove_alert_recipients_alter_alert_files'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='files',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]
