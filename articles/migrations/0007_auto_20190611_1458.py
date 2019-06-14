# Generated by Django 2.2 on 2019-06-11 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_advuser_activity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advuser',
            name='bio',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Биография'),
        ),
        migrations.AlterField(
            model_name='advuser',
            name='status',
            field=models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='Статус'),
        ),
    ]