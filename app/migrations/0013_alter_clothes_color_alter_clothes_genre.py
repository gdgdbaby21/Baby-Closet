# Generated by Django 5.0.7 on 2024-11-20 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_alter_clothes_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clothes',
            name='color',
            field=models.CharField(choices=[('white', '白'), ('black', '黒'), ('gray', 'グレー'), ('brown', '茶'), ('beige', 'ベージュ'), ('green', '緑'), ('blue', '青'), ('purple', '紫'), ('yellow', '黄'), ('pink', 'ピンク'), ('red', '赤'), ('orange', 'オレンジ'), ('other', 'その他')], max_length=10),
        ),
        migrations.AlterField(
            model_name='clothes',
            name='genre',
            field=models.CharField(choices=[('tops', 'トップス'), ('skirts', 'スカート'), ('outer', 'アウター'), ('onepiece', 'ワンピース'), ('pants', 'パンツ'), ('hat', '帽子'), ('maternity', 'マタニティ'), ('other', 'その他')], max_length=20),
        ),
    ]