from django.contrib import admin

from .models import AdvUser, Category, Article, Gender


def activate_articles(modeladmin, request, queryset):
    for rec in queryset:
        if not rec.is_active:
            rec.is_active = True
            rec.save()
    modeladmin.message_user(request, 'Выбранные статьи активированы.')
    

activate_articles.short_description = 'Активация выбранных статей (пометка как модерированных).'


# Gender admin panel.
class GenderAdmin(admin.ModelAdmin):
    list_display = ('name', 'one_letter_name', )


admin.site.register(Gender, GenderAdmin)


# User admin panel.
class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'company', 'is_activated', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fields = (('username', 'email'),
              'gender',
              ('first_name', 'last_name'),
              ('account_image', 'account_image_url', 'admin_image'),
              'company',
              'activity',
              'country', 'city',
              'bdate',
              'fb_url',
              'tw_url',
              'vk_url',
              'ok_url',
              'bio',
              'status',
              'user_subscriptions',
              'tags_subscriptions',
              'rating',
              'send_messages',
              'is_activated',
              'is_active',
              ('is_staff', 'is_superuser'),
              'groups',
              'date_joined',
              'last_login')
    filter_horizontal = ('groups', )
    readonly_fields = ('last_login', 'date_joined', 'admin_image')
    

admin.site.register(AdvUser, AdvUserAdmin)


# Category admin panel.
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('name', )


admin.site.register(Category, CategoryAdmin)


# Article admin.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'created_at', 'total_rating', 'is_active', )
    # filter_horizontal = ('tags', )
    search_fields = ('title', 'rubric', )
    readonly_fields = ('views',
                       'created_at',
                       )
    actions = (activate_articles, )
    
    
admin.site.register(Article, ArticleAdmin)
