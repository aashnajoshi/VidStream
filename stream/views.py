from django.shortcuts import render, get_object_or_404
from .models import Stream

# Display list of streams on home page
def home(request):
    allStreams = Stream.objects.all()  # Fetch all streams
    return render(request, 'stream/stream.html', context={'title': 'Home', 'allStreams': allStreams})

# Display details of a specific stream
def stream(request, slug):
    stream = get_object_or_404(Stream, slug=slug)  # Fetch stream by slug
    return render(request, 'stream/stream.html', context={'title': stream.title, 'stream': stream})

# Display the video play page
def video_play(request, id):
    stream = get_object_or_404(Stream, id=id)  # Fetch stream by id
    return render(request, 'stream/stream.html', context={'title': stream.title, 'stream': stream, 'play_video': True})