# Generated by Django 2.2 on 2019-05-13 05:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_article_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='tag1',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='articles.Tag', verbose_name='Тег'),
        ),
    ]
