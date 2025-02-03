from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page (list of all streams)
    path('<str:slug>/', views.stream, name='stream'),  # Specific stream details
    path('play/<int:id>/', views.video_play, name='video_play'),  # Play video
]