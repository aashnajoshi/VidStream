from django.urls import path
from home.views import SearchView, SignInView
from .views import HomeView, UploadVideoView, VideoPlayView, CreateOrJoinRoomView, WatchRoomView, RoomView, LeaveRoomView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('upload/', UploadVideoView.as_view(), name='upload'),
    path('search/', SearchView.as_view(), name='search'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('play/<int:video_id>/', VideoPlayView.as_view(), name='video_play'),
    path('create-or-join-room/', CreateOrJoinRoomView.as_view(), name='create_or_join_room'),
    path('room/<str:room_code>/<int:video_id>/', WatchRoomView.as_view(), name='room_watch'),
    path('room/<str:room_code>/', RoomView.as_view(), name='room_view'),
    path('room/<str:room_code>/leave/', LeaveRoomView.as_view(), name='leave_room'),
]