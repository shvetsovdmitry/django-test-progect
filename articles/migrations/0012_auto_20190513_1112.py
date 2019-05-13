# Generated by Django 2.2 on 2019-05-13 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0011_auto_20190513_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='card_text',
            field=models.TextField(blank=True, null=True, verbose_name='Аннотация'),
        ),
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Изображение'),
        ),
    ]
