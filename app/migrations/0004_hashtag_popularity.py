# Generated by Django 5.0.7 on 2024-12-04 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_comment_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='hashtag',
            name='popularity',
            field=models.IntegerField(default=0),
        ),
    ]
