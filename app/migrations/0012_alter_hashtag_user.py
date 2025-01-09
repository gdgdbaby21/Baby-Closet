# Generated by Django 5.0.7 on 2025-01-08 02:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_clothes_created_at_hashtag_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hashtag',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
