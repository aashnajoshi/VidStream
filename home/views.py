from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home/index.html', context={'title': 'Home'})

def about(request):
    return render(request, 'home/index.html', context={'title': 'About'})