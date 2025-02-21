from django.urls import path
from .views import *
from home.views import signin, search

urlpatterns = [
    path('', home, name='home'),
    path('upload/', upload_video, name='upload'),
    path('search/', search, name='search'),
    path('login/', signin, name='login'),
    path('play/<int:video_id>/', video_play, name='video_play'), 
    path('create-or-join-room/', create_or_join_room, name='create_or_join_room'),
    path('room/<str:room_code>/<int:video_id>/', watch_room, name='room_watch'),
    path('room/<str:room_code>/leave/', leave_room, name='leave_room'),
]