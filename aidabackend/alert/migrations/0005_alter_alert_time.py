# Generated by Django 5.1.2 on 2024-10-15 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0004_alert_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
