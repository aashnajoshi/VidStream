from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Contact

@admin.register(Contact)
class ContactAdmin(ModelAdmin):
    list_display = ('name', 'email', 'message', 'file_path', 'created_at')
    search_fields = ('name', 'email', 'message')
    list_filter = ('name','created_at')