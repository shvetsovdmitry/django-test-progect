from django.contrib.auth.models import AbstractUser
from django.db import models
from pipenv.vendor.cerberus.errors import MAX_LENGTH
import os

class AdvUser (AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Активирован?')
    send_messages = models.BooleanField(default=True, verbose_name='Присылать сообщения о новых комментариях?')

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


def get_image_path(instance, filename):
    return os.path.join('images', str(instance.id), filename)


@property
def image_url(self):
    if self.image and hasattr(self.image, 'url'):
        return self.image.url


class Article (models.Model):
    category = models.ForeignKey(Category, default=None, on_delete=models.PROTECT, verbose_name='Категория')
    title = models.CharField(max_length=40, verbose_name='Название статьи')
    content = models.TextField(verbose_name='Содержание')
    image = models.ImageField(verbose_name='Изображение', blank=True, null=True, upload_to=get_image_path)
    card_text = models.TextField(verbose_name='Аннотация', blank=True, null=True)
    author = models.ForeignKey(AdvUser, on_delete=models.PROTECT, verbose_name='Автор')
    tags = models.ManyToManyField(Tag, verbose_name='Теги')
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
