from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    return render(request, 'home/index.html', context={'title': 'Home'})

def about(request):
    return render(request, 'home/index.html', context={'title': 'About'})

def contact(request):
    if request.method == 'POST':
        user_email = request.POST.get('email')
        user_subject = request.POST.get('subject')
        user_message = request.POST.get('message')

        subject = f"New Contact Form Submission: {user_subject}"
        message = f"Message from {user_email}:\n\n{user_message}"
        recipient_list = [settings.EMAIL_HOST_USER]

        try:
            email = EmailMessage(subject, message, user_email, recipient_list)
            email.send()
            messages.success(request, 'Your message has been sent successfully!')
        except Exception as e:
            messages.error(request, f'Error sending email: {e}')
        return redirect('contact')

    else:
        return render(request, 'home/index.html', context={'title': 'Contact'})
