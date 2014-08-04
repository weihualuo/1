from django.contrib import admin
from django.utils.translation import ugettext as _
from templates.models import *

# Register your models here.
class TemplateAdmin(admin.ModelAdmin):

    fieldsets = [
        (None,               {'fields': ['title', 'desc', 'style', 'image']}),
        (_('Other Info'), {'fields': ['meta', 'array', 'credit', 'author'], 'classes': ['collapse']}),
    ]

    list_display = ['title', 'desc', 'uri', 'image', 'style', 'author', 'credit']
    search_fields = ['title']

class StyleAdmin(admin.ModelAdmin):
    list_display = ['en', 'cn']

admin.site.register(Template, TemplateAdmin)
admin.site.register(Style, StyleAdmin)