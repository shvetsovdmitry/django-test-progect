from django.contrib import admin
from .models import Company

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', )
    search_fields = ('name', )
    # fieldsets = ('__all__', )
    fields = (
            'name',
            'description',
            ('logo_url', 'logo_preview'),
            'created_at',
        )
    readonly_fields = ('logo_preview', 'created_at')
        

admin.site.register(Company, CompanyAdmin)
