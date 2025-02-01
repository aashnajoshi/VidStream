from django.shortcuts import render, HttpResponse

# Create your views here.
def home(request):
    return render(request, 'stream/stream.html', context={'title': 'Home'})

def stream(request, slug):
    post = Post.objects.get(slug=slug)[0]
    if post:
        return render(request, 'stream/stream.html', context={'title': post.title, 'post': post})
    else:
        return HttpResponse(f"Stream Title: {slug}")