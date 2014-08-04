from django.contrib import admin

from users.models import *

class UserProfileAdmin(admin.ModelAdmin):

    list_display = ["user", "status", "gender", "desc"]
    search_fields = ["user"]

admin.site.register(Profile, UserProfileAdmin)
