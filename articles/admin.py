from django.contrib import admin

from .models import AdvUser, Category, Article, Tag, Gender
# from .models import ArticleStatistics


class GenderAdmin(admin.ModelAdmin):
    # model = Gender
    list_display = ('name',)

admin.site.register(Gender, GenderAdmin)

# User model admin
class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_activated', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fields = (('username', 'email'),
              'gender',
              ('first_name', 'last_name'),
              ('account_image', 'admin_image'),
              'fb_url',
              'tw_url',
              'vk_url',
              'ok_url',
              'send_messages',
              'is_activated',
              'is_active',
              ('is_staff', 'is_superuser'),
              'groups',
              'date_joined',
              'last_login')
    filter_horizontal = ('groups', )
    readonly_fields = ('last_login', 'date_joined', 'admin_image')
    # inlines = (GenderAdmin,)
    

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
    list_display = ('title', 'category', 'author', 'created_at', 'total_rating', 'rating_count', 'is_active', )
    filter_horizontal = ('tags', )
    search_fields = ('title', 'rubric', )
    readonly_fields = ('views',
                       'created_at',
                    #    'rating_count'
                       )
    
    
admin.site.register(Article, ArticleAdmin)


# class ArticleStatisticsAdmin(admin.ModelAdmin):
#     list_display = ('__str__', 'rating', 'views')
#     search_fields = ('__str__', )
    

# admin.site.register(ArticleStatistics, ArticleStatisticsAdmin)
