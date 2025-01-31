from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import ContactUs

# Create your views here.
def home(request):
    return render(request, 'home/index.html', context={'title': 'Home'})

def about(request):
    return render(request, 'home/index.html', context={'title': 'About'})

def contact(request):
    if request.method == 'POST':
        user_name = request.POST.get('name')
        user_email = request.POST.get('email')
        user_message = request.POST.get('message')
        attachment = request.FILES.get('file_path')
        contact = ContactUs(name=user_name, email=user_email, message=user_message, file_path=attachment)
        contact.save()
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')
    else:
        return render(request, 'home/index.html', context={'title': 'Contact'})