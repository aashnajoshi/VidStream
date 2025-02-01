from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Contact

# Create your views here.
def home(request):
    return render(request, 'home/home.html', context={'title': 'Home'})

def about(request):
    return render(request, 'home/about.html', context={'title': 'About'})

def contact(request):
    if request.method == 'POST':
        user_name = request.POST.get('name')
        user_email = request.POST.get('email')
        user_message = request.POST.get('message')
        attachment = request.FILES.get('file_path')
        contact = Contact(name=user_name, email=user_email, message=user_message, file_path=attachment)
        if len(user_name)<2 or len(user_email)<3 or len(user_message)<4:
            messages.error(request, 'Invalid form data!')
        else:
            contact.save()
            messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')
    else:
        return render(request, 'home/contact.html', context={'title': 'Contact'})