# Generated by Django 5.0.7 on 2024-11-15 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_wishlistitem_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlistitem',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='wishlist_images/'),
        ),
    ]
