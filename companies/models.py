from django.db import models
from django.utils.html import format_html
from django.utils import timezone

class Company(models.Model):
    name = models.CharField(default='', max_length=100, verbose_name='Название компании', unique=True)
    # logo = models.ImageField(blank=True, null=True, verbose_name='Логотип компании')
    logo_url = models.URLField(default='', blank=True, null=True, verbose_name='Ссылка на логотип компании')
    description = models.TextField(default='', blank=True, null=True, verbose_name='Описание компании')
    
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата добавления')
    
    def logo_preview(self):
        if self.logo:
            return format_html('<img src="%s" style="width:300px; height: 200px" />' % self.logo.url)
        elif self.logo_url:
            return format_html('<img src="%s" style="width:300px; height: 200px" />' % self.logo_url)
    logo_preview.short_description = 'Превью'
    logo_preview.allow_tags = True
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'
    