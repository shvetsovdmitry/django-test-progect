from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import Signal
from django.utils import timezone
from django.utils.html import format_html

from companies.models import Company

from django_countries.fields import CountryField
from tagging.models import Tag
from tagging_autocomplete_new.models import TagAutocompleteField

from .utilities import send_activation_notification
import os


# Returns image path in media folder.
def get_image_path(instance, filename):
    return os.path.join('images', str(instance.id), filename)


user_registrated = Signal(providing_args=['instance'])


def user_registrated_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])
    

user_registrated.connect(user_registrated_dispatcher)


# Gender model.
class Gender (models.Model):
    name = models.CharField(max_length=20, default=None, db_index=True, unique=True, verbose_name='Название')
    one_letter_name = models.CharField(max_length=1, default=None, unique=True, verbose_name='Название пола в одну букву', help_text='Используется в коде.')
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Гендер'
        verbose_name_plural = 'Гендеры'


# Category model.
class Category (models.Model):
    name = models.CharField(max_length=20, default=None, db_index=True, unique=True, verbose_name='Название')
    order = models.SmallIntegerField(default=0, db_index=True, verbose_name='Порядок')
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('order', 'name')
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        

class Notification(models.Model):
    content = models.CharField(max_length=50, default='', verbose_name='Содержимое')
    viewed = models.BooleanField(default=False, verbose_name='Просмотрено')
    
    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
    

# User model.
class AdvUser (AbstractUser):
    # Socials.
    vk_url = models.URLField(default="", blank=True, verbose_name='ВКонтакте')
    fb_url = models.URLField(default="", blank=True, verbose_name='Facebook')
    tw_url = models.URLField(default="", blank=True, verbose_name='Twitter')
    ok_url = models.URLField(default="", blank=True, verbose_name='Одноклассники')
    # Personal.
    bio = models.TextField(default='', blank=True, verbose_name='Биография')
    status = models.CharField(default='', blank=True, max_length=200, verbose_name='Статус')
    company = models.ForeignKey(Company, default=None, blank=True, null=True, on_delete=models.PROTECT, verbose_name='Компания')
    activity = models.CharField(max_length=100, default='', blank=True, verbose_name='Деятельность')
    
    account_image = models.ImageField(blank=True, null=True, upload_to=get_image_path, verbose_name='Изображение профиля', help_text='Лучше всего подобрать картинку с соотношением сторон 4:3.')
    account_image_url = models.URLField(default="", blank=True, verbose_name='Ссылка на изображение профиля', help_text='Вы можете либо загрузить картинку, либо вставить ссылку на нее.')
    country = CountryField(blank_label='Выберите страну', blank=True, null=True, verbose_name='Страна')
    city = models.CharField(blank=True, null=True, max_length=50, verbose_name='Город')
    bdate = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    gender = models.ForeignKey(Gender, default=None, blank=True, null=True, on_delete=models.PROTECT, verbose_name='Пол')
    user_subscriptions = models.ManyToManyField('self', related_name='user_subscriptions', blank=True, verbose_name='Подписки на пользователей')
    tags_subscriptions = models.ManyToManyField(Tag, related_name='tags_subscriptions', blank=True, verbose_name='Подписки на теги')
    cat_subscriptions = models.ManyToManyField(Category, related_name='cat_subscriptions', blank=True, verbose_name='Подписки на категории')
    notifications = models.ManyToManyField(Notification, related_name='notifications', blank=True, verbose_name='Уведомления')
    # User's rating.
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    # System.
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Активирован?', help_text='Пользователю было отправлено письмо на почту с ссылкой для активации аккаунта.')
    send_messages = models.BooleanField(default=True, verbose_name='Присылать сообщения о новых комментариях?')

    # account_image preview in admin site.
    def admin_image(self):
        if self.account_image:
            return format_html('<img src="%s" style="width:400px; height: 200px" />' % self.account_image.url)
        elif self.account_image_url:
            return format_html('<img src="%s" style="width:400px; height: 200px" />' % self.account_image_url)
    admin_image.short_description = 'Превью'
    admin_image.allow_tags = True

    def subscribe_user(self, user: 'self'):
        self.user_subscriptions.add(user)
        self.save()
        
    def unsubscribe_user(self, user: 'self'):
        self.user_subscriptions.remove(user)
        self.save()
        
    def subscribe_tag(self, tag: Tag):
        self.tags_subscriptions.add(tag)
        self.save()
        
    def unsubscribe_tag(self, tag: Tag):
        self.tags_subscriptions.remove(tag)
        self.save()

    def subscribe_category(self, category: Category):
        self.cat_subscriptions.add(category)
        self.save()
        
    def unsubscribe_category(self, category: Category):
        self.cat_subscriptions.remove(category)
        self.save()

    class Meta :
       verbose_name = 'Пользователь'
       verbose_name_plural = 'Пользователи'


# Article model.
class Article (models.Model):
    category = models.ForeignKey(Category, default=None, on_delete=models.PROTECT, verbose_name='Категория')
    title = models.CharField(max_length=100, verbose_name='Название статьи', help_text='Введите до 100 символов.')
    content = models.TextField(verbose_name='Содержание')
    # Preview image. Will be on index page and on top of article page.
    image = models.ImageField(verbose_name='Превью',
                              blank=True,
                              null=True,
                              upload_to=get_image_path,
                              help_text="""Изображение на плитке на главной странице.
                              Это поле проверяется первым.
                              Если файл отсутствует - получает картинку по ссылке (ниже).""")
    # If image does not exists - load image_url.
    image_url = models.TextField(verbose_name='Ссылка на изображение',
                                blank=True,
                                null=True,
                                help_text='Изображение на плитке на главной странице.')
    # Text on card on index page.
    card_text = models.TextField(verbose_name='Аннотация', blank=True, null=True, max_length=200, help_text='Введите до 200 символов.')
    author = models.ForeignKey(AdvUser, on_delete=models.PROTECT, verbose_name='Автор')
    tags = TagAutocompleteField(blank=True, null=True)
    # Total article rating (sum of all votes).
    total_rating = models.IntegerField(verbose_name='Всего баллов', default=0, help_text='Всего баллов, полученных от пользователей')
    # Current rating (total_rating/rating_count).
    rating = models.FloatField(verbose_name='Текущий рейтинг', default=0, help_text='Текущий рейтинг в 5-ти балльной шкале', max_length=1)
    # Number of views.
    views = models.IntegerField(verbose_name='Просмотры', default=0)
    # Users who vote for article.
    rated_users = models.ManyToManyField(AdvUser, related_name='rated_users',  verbose_name='Проголосовавшие пользователи', blank=True)
    # Users who read article.
    viewed_users = models.ManyToManyField(AdvUser, related_name='viewed_users', verbose_name='Пользователи, читавшие статью', blank=True)
    # System.
    is_active = models.BooleanField(default=False, verbose_name='Прошла ли модерацию?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    
    def __str__(self):
        return self.title
    
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
    
    # When user press rating button.
    def change_rating(self, rating, user):
        if len(self.rated_users.all()) > 0:
            self.total_rating += rating
            self.rating = round(self.total_rating/(len(self.rated_users.all()) + 1), 2)
        else:
            self.rating = rating
            self.total_rating = rating
        self.rated_users.add(user)            
        self.save()

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
