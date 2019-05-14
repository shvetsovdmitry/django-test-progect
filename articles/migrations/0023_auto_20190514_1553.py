# Generated by Django 2.2 on 2019-05-14 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0022_advuser_account_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(db_index=True, default=None, max_length=20, unique=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Пол',
            },
        ),
        migrations.AddField(
            model_name='advuser',
            name='bdate',
            field=models.DateField(blank=True, null=True, verbose_name='Дата рождения'),
        ),
        migrations.AddField(
            model_name='advuser',
            name='city',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Город'),
        ),
        migrations.AddField(
            model_name='advuser',
            name='fb_url',
            field=models.URLField(blank=True, null=True, verbose_name='Facebook'),
        ),
        migrations.AddField(
            model_name='advuser',
            name='ok_url',
            field=models.URLField(blank=True, null=True, verbose_name='Одноклассники'),
        ),
        migrations.AddField(
            model_name='advuser',
            name='rating',
            field=models.IntegerField(default=0, verbose_name='Рейтинг'),
        ),
        migrations.AddField(
            model_name='advuser',
            name='tw_url',
            field=models.URLField(blank=True, null=True, verbose_name='Twitter'),
        ),
        migrations.AddField(
            model_name='advuser',
            name='vk_url',
            field=models.URLField(blank=True, null=True, verbose_name='ВКонтакте'),
        ),
        migrations.AlterField(
            model_name='advuser',
            name='is_activated',
            field=models.BooleanField(db_index=True, default=True, help_text='Пользователю было отправлено письмо на почту с ссылкой для активации аккаунта.', verbose_name='Активирован?'),
        ),
        migrations.AddField(
            model_name='advuser',
            name='gender',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.PROTECT, to='articles.Gender', verbose_name='Пол'),
        ),
    ]
