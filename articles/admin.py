from django.contrib import admin

from .models import AdvUser, Rubric, Article


class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_activated', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fields = (('username', 'email'),
              ('first_name', 'last_name'),
              ('send_messages', 'is_activated', 'is_active'),
              ('is_staff', 'is_superuser'),
              'groups', 'user_permissions',
              ('last_login', 'date_joined'))
    readonly_fields = ('last_login', 'date_joined')
    

admin.site.register(AdvUser, AdvUserAdmin)


class RubricAdmin(admin.ModelAdmin):
    model = Rubric
    list_display = ('name',)
    
    
admin.site.register(Rubric, RubricAdmin)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('rubric', 'title', 'author', 'created_at', 'is_active')
    search_fields = ('title',)
    readonly_fields = ('created_at', )
    
    
admin.site.register(Article, ArticleAdmin)
    