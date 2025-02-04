from django.urls import path
from . import views
from home.views import signin, search

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_video, name='upload'),
    path('search/', search, name='search'),
    path('login/', signin, name='login'),
    path('play/<int:video_id>/', views.video_play, name='video_play'),
]