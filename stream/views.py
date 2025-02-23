import random
import string
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from .models import Comment, Room, Stream

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

    if request.method == 'POST':
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')
        if content:
            if parent_id:
                try:
                    parent_comment = Comment.objects.get(id=parent_id)
                    comment = Comment(video=video, user=request.user, content=content, parent=parent_comment)
                except Comment.DoesNotExist:
                    messages.error(request, "Parent comment does not exist.")
                    return redirect('video_play', video_id=video_id)
            else:
                comment = Comment(video=video, user=request.user, content=content)
            comment.save()
            messages.success(request, 'Your comment has been posted!')

    comments = video.comments.filter(parent=None).order_by('-created_at')
    return render(request, 'stream/watch.html', context={'video': video, 'videos': other_videos, 'comments': comments})

@login_required
def create_or_join_room(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        room_code = request.POST.get('room_code').lower()

        if action == 'create':
            room_code = generate_room_code()
            room = Room.objects.create(room_code=room_code)
            room.users.add(request.user)
            room.save()

            messages.success(request, f"Room created with code: {room_code}")
            video = Stream.objects.first()
            if not video:
                messages.error(request, "No videos available to select.")
                return redirect('home')
            video_id = video.id
            return redirect('room_watch', room_code=room_code, video_id=video_id)

        elif action == 'join':
            try:
                room = Room.objects.get(room_code=room_code)
                room.users.add(request.user)
                room.save()

                messages.success(request, f"Joined room: {room_code}")
                video = Stream.objects.first()
                if not video:
                    messages.error(request, "No videos available to select.")
                    return redirect('home')
                video_id = video.id
                return redirect('room_watch', room_code=room_code, video_id=video_id)

            except Room.DoesNotExist:
                messages.error(request, f"Room with code {room_code} does not exist.")
                return redirect('home')
    return redirect('home')

@login_required
def watch_room(request, room_code, video_id):
    try:
        room = Room.objects.get(room_code=room_code)   
        if request.user not in room.users.all():
            room.users.add(request.user)
            room.save()
            messages.success(request, f"You have been added to the room {room_code}")

        video = Stream.objects.get(id=video_id)
        video.views += 1
        video.save()
        other_videos = Stream.objects.exclude(id=video_id)

        return render(request, 'stream/stream.html', {'room': room, 'video': video, 'videos': other_videos})

    except Room.DoesNotExist:
        messages.error(request, "Room does not exist.")
        return redirect('home')
    except Stream.DoesNotExist:
        messages.error(request, "Video does not exist.")
        return redirect('home')

def room_view(request, room_code):
    room = get_object_or_404(Room, room_code=room_code)
    return render(request, 'stream/room.html', {'room': room})

def generate_room_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

def leave_room(request, room_code):
    room = get_object_or_404(Room, room_code=room_code)
    room.users.remove(request.user)
    if room.users.count() == 0:
        room.delete()
    return redirect('home')