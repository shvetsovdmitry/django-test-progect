# Generated by Django 2.2 on 2019-05-13 04:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_auto_20190513_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='tag1',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tag1', to='articles.Tag', verbose_name='Тег'),
        ),
        migrations.AlterField(
            model_name='article',
            name='tag2',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tag2', to='articles.Tag', verbose_name='Тег'),
        ),
        migrations.AlterField(
            model_name='article',
            name='tag3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tag3', to='articles.Tag', verbose_name='Тег'),
        ),
    ]
