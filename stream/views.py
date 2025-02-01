from django.shortcuts import render, HttpResponse

# Create your views here.
def home(request):
    return render(request, 'stream/stream.html', context={'title': 'Home'})

def stream(request, slug):
    return HttpResponse(f"Stream Title: {slug}")