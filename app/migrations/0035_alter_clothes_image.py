# Generated by Django 5.0.7 on 2025-02-26 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0034_alter_user_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clothes',
            name='image',
            field=models.ImageField(null=True, upload_to='clothes_images/'),
        ),
    ]
