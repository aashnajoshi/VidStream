from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import random
import string

def home(request):
    videos = Stream.objects.all().order_by('-created_at')
    paginator = Paginator(videos, 30)
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'stream/home.html', context={'videos': page_obj})

@login_required
def upload_video(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        cover_image = request.FILES.get('cover_image')
        video_file = request.FILES.get('video_file')
        trailer_link = request.POST.get('trailer_link')
        genre = request.POST.get('genre')
        description = request.POST.get('description')

        stream = Stream(title=title, cover_image=cover_image, video_file=video_file, trailer_link=trailer_link, genre=genre, description=description, uploaded_by=request.user.username)
        stream.save()
        messages.success(request, 'Video uploaded successfully')

        return redirect('home')
    return render(request, 'stream/upload.html')

@login_required
def video_play(request, video_id):
    try:
        video = Stream.objects.get(id=video_id)
        video.views += 1
        video.save() 
    except Stream.DoesNotExist:
        return redirect('home')
    
    other_videos = Stream.objects.exclude(id=video_id)

    if request.method == 'POST': # For Comments
        content = request.POST.get('content')
        if content:
            comment = Comment(video=video, user=request.user, content=content)
            comment.save()
            messages.success(request, 'Your comment has been posted!')

    comments = video.comments.all().order_by('-created_at')

    return render(request, 'stream/watch.html', context={'video': video, 'videos': other_videos, 'comments': comments})

def generate_room_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@login_required
def create_or_join_room(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        room_code = request.POST.get('room_code').lower()

        # If action is to create a new room
        if action == 'create':
            # Generate a unique room code
            room_code = generate_room_code()
            room = Room.objects.create(room_code=room_code)
            room.users.add(request.user)
            room.save()

            messages.success(request, f"Room created with code: {room_code}")
            return redirect('room_watch', room_code=room_code)

        # If action is to join an existing room
        elif action == 'join':
            try:
                room = Room.objects.get(room_code=room_code)
                room.users.add(request.user)
                room.save()

                messages.success(request, f"Joined room: {room_code}")
                return redirect('room_watch', room_code=room_code)

            except Room.DoesNotExist:
                messages.error(request, f"Room with code {room_code} does not exist.")
                return redirect('home')
    return redirect('home')

@login_required
def watch_room(request, room_code):
    try:
        room = Room.objects.get(room_code=room_code)
        videos = Video.objects.all()
        return render(request, 'stream/watch_room.html', {'room': room, 'videos': videos})
    except Room.DoesNotExist:
        messages.error(request, "Room does not exist.")
        return redirect('home')