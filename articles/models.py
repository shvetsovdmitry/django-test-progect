from django.db import models
from django.contrib.auth.models import AbstractUser


class AdvUser (AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Активирован?')
    send_messages = models.BooleanField(default=True, verbose_name='Присылать сообщения о новых комментариях?')

    class Meta :
       verbose_name = 'Пользователь'
       verbose_name_plural = 'Пользователи'


class Rubric (models.Model):
    name = models.CharField(max_length=20, db_index=True, unique=True, verbose_name='Название')
    order = models.SmallIntegerField(default=0, db_index=True, verbose_name='Порядок')
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('order', 'name')
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Article (models.Model):
    rubric = models.ForeignKey(Rubric, on_delete=models.PROTECT, verbose_name='Рубрика')
    title = models.CharField(max_length=40, verbose_name='Название статьи')
    content = models.TextField(verbose_name='Содержание')
    author = models.ForeignKey(AdvUser, on_delete=models.PROTECT, verbose_name='Автор')
    is_active = models.BooleanField(default=False, verbose_name='Прошла ли модерацию?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    
    def __str__(self):
        return self.title
    
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
