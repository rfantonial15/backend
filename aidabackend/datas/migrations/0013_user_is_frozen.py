# Generated by Django 5.1.1 on 2024-11-26 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datas', '0012_user_is_staff_alter_user_is_superuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_frozen',
            field=models.BooleanField(default=False),
        ),
    ]