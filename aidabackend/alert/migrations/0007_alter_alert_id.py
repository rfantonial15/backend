# Generated by Django 5.1.1 on 2024-10-17 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0006_alter_alert_image_alter_alert_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
