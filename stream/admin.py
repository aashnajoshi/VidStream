from django.contrib import admin
from django.db import models
from .models import *

class StreamAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'created_at')
    search_fields = ('title', 'genre', 'description')
    list_filter = ('genre', 'created_at')
    
admin.site.register(Stream, StreamAdmin)