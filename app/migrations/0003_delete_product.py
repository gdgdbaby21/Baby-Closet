# Generated by Django 5.0.7 on 2024-11-12 14:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_product'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Product',
        ),
    ]