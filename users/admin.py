from django.contrib import admin
from .models import CustomUsers

class UsersAdmin(admin.ModelAdmin):
    pass

admin.site.register(CustomUsers, UsersAdmin)
