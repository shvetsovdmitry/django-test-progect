# Generated by Django 2.2 on 2019-05-13 06:57

import articles.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0013_auto_20190513_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, height_field=400, null=True, upload_to=articles.models.get_image_path, verbose_name='Изображение', width_field=400),
        ),
    ]
