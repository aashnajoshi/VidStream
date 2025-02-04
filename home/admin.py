from django.contrib import admin
from django.db import models
from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'file_path', 'date_added')
    search_fields = ('name', 'email', 'message')
    list_filter = ('name','date_added')

admin.site.register(Contact, ContactAdmin)