from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import Signal
from django.utils.safestring import mark_safe
from .utilities import send_activation_notification
import os


def get_image_path(instance, filename):
    return os.path.join('images', str(instance.id), filename)


user_registrated = Signal(providing_args=['instance'])


def user_registrated_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])
    

user_registrated.connect(user_registrated_dispatcher)


class AdvUser (AbstractUser):
    account_image = models.ImageField(blank=True, null=True, upload_to=get_image_path, verbose_name='Аватар')
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Активирован?')
    send_messages = models.BooleanField(default=True, verbose_name='Присылать сообщения о новых комментариях?')

    def admin_image(self):
        return mark_safe('<img src="%s" style="width:300px; height: 200px" />' % self.account_image.url)
    admin_image.short_desctiption = 'Предпросмотр аватара'
    admin_image.allow_tags = True

    class Meta :
       verbose_name = 'Пользователь'
       verbose_name_plural = 'Пользователи'


class Category (models.Model):
    name = models.CharField(max_length=20, default=None, db_index=True, unique=True, verbose_name='Название')
    order = models.SmallIntegerField(default=0, db_index=True, verbose_name='Порядок')
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('order', 'name')
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Tag (models.Model):
    name = models.CharField(max_length=20, db_index=True, unique=True, verbose_name='Название')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']


class Article (models.Model):
    category = models.ForeignKey(Category, default=None, on_delete=models.PROTECT, verbose_name='Категория')
    title = models.CharField(max_length=40, verbose_name='Название статьи')
    content = models.TextField(verbose_name='Содержание')
    image = models.ImageField(verbose_name='Изображение', blank=True, null=True, upload_to=get_image_path)
    image_url = models.URLField(verbose_name='Ссылка на изображение', blank=True, null=True)
    card_text = models.TextField(verbose_name='Аннотация', blank=True, null=True)
    author = models.ForeignKey(AdvUser, on_delete=models.PROTECT, verbose_name='Автор')
    tags = models.ManyToManyField(Tag, verbose_name='Теги', blank=True)
    rating = models.FloatField(verbose_name='Рейтинг', max_length=10, default=0)
    is_active = models.BooleanField(default=False, verbose_name='Прошла ли модерацию?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    
    def __str__(self):
        return self.title
    
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
