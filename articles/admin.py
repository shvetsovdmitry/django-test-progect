from django.contrib import admin

from .models import AdvUser, Category, Article, Tag


# User model admin
# @admin.site.register(AdvUser)
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


# Category admin.
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('name', )
    
    
admin.site.register(Category, CategoryAdmin)


# Tag admin
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )
    

admin.site.register(Tag, TagAdmin)


# Article admin
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'created_at', 'rating', 'is_active', )
    filter_horizontal = ('tags', )
    search_fields = ('title', 'rubric', )
    readonly_fields = ('created_at', )
    
    
admin.site.register(Article, ArticleAdmin)
