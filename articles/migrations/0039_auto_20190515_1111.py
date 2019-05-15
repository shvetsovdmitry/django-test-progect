# Generated by Django 2.2 on 2019-05-15 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0038_auto_20190515_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='rating',
            field=models.FloatField(default=0, help_text='Текущий рейтинг в 5-ти балльной шкале', max_length=1, verbose_name='Текущий рейтинг'),
        ),
    ]
