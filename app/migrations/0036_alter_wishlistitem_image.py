# Generated by Django 5.0.7 on 2025-02-26 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0035_alter_clothes_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlistitem',
            name='image',
            field=models.ImageField(default='wishlist_images/default.png', null=True, upload_to='wishlist_images/'),
        ),
    ]
