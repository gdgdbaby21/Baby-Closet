# Generated by Django 5.0.7 on 2025-02-06 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_alter_clothes_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clothes',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='clothes_images/'),
        ),
    ]
