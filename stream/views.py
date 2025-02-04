from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Stream
from django.contrib import messages

def home(request):
    videos = Stream.objects.all()
    paginator = Paginator(videos, 30)
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'stream/stream.html', context={'videos': page_obj})

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
        print(video)
    except Stream.DoesNotExist:
        return redirect('stream')
    
    return render(request, 'stream/watch.html', context={'video': video})