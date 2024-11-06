# Generated by Django 5.0.7 on 2024-11-06 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_delete_wishlistitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='WishlistItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('画像', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('値段', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ブランド', models.CharField(max_length=50)),
                ('商品URL', models.URLField()),
                ('メモ', models.TextField(blank=True)),
            ],
        ),
    ]
