from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import *

@admin.register(Stream)
class StreamAdmin(ModelAdmin):
    list_display = ('title', 'genre', 'created_at')
    search_fields = ('title', 'genre', 'description')
    list_filter = ('genre', 'created_at')

admin.site.register(Comment)
admin.site.register(Room)