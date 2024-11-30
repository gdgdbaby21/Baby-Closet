# Generated by Django 5.0.7 on 2024-11-30 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='hashtags',
            field=models.ManyToManyField(blank=True, to='app.hashtag'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='wishlistitem',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=10),
        ),
    ]
