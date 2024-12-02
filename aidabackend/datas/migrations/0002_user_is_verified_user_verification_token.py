# Generated by Django 5.1.1 on 2024-11-08 05:41

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='verification_token',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
