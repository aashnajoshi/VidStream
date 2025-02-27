from django.contrib.admin import register
from unfold.admin import ModelAdmin
from .models import *

@register(Stream)
class StreamAdmin(ModelAdmin):
    list_display = ('title', 'genre', 'created_at', 'uploaded_by', 'views')
    search_fields = ('title', 'genre', 'description')
    list_filter = ('genre', 'created_at')

@register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ('video', 'user', 'content', 'created_at')
    search_fields = ('video', 'user', 'created_at')
    list_filter = ('video', 'user', 'created_at')

@register(Room)
class RoomAdmin(ModelAdmin):
    list_display = ('room_code', 'created_at')
    search_fields = ('room_code', 'created_at')
    list_filter = ('room_code', 'created_at')