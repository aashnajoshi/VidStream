from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Contact
from stream.models import Stream
import re

# Home View
def home(request):
    return render(request, 'home/home.html', context={'title': 'Home'})

# About View
def about(request):
    return render(request, 'home/about.html', context={'title': 'About'})

# Contact View
def contact(request):
    if request.method == 'POST':
        user_name = request.POST.get('name')
        user_email = request.POST.get('email')
        user_message = request.POST.get('message')
        attachment = request.FILES.get('file_path')
        
        if request.user.is_authenticated:
            user_name = request.user.username
            user_email = request.user.email

        if not request.user.is_authenticated:
            if len(user_name) < 2 or not re.match(r"[^@]+@[^@]+\.[^@]+", user_email) or len(user_message) < 4:
                messages.error(request, 'Invalid form data! Please check your name, email, and message.')
                return redirect('contact')
        contact = Contact(name=user_name, email=user_email, message=user_message, file_path=attachment)
        contact.save()
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')
    else:
        context = {'title': 'Contact'}
        if request.user.is_authenticated:
            context['user_name'] = request.user.username
            context['user_email'] = request.user.email
        return render(request, 'home/contact.html', context)

# Search View
def search(request):
    query = request.GET.get('query')
    if len(query) > 78:
        allStreams = []
    else:
        allStreamsTitle = [stream.title for stream in Stream.objects.all()]
        allStreamsDescription = [stream.description for stream in Stream.objects.all()]
        allStreamsGenre = [stream.genre for stream in Stream.objects.all()]
        
        allStreams = [stream for stream in Stream.objects.all() if query.lower() in stream.title.lower() or query.lower() in stream.description.lower() or query.lower() in stream.genre.lower()]

    if len(allStreams) == 0:
        messages.warning(request, f'No search results found for "{query}". Please refine your query.')

    return render(request, 'home/search.html', context={'title': 'Search', 'allStreams': allStreams, 'query': query})

# SignUp View
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmPassword']

        # Basic form validation
        if len(username) < 4 or len(password) < 4 or username.isalnum() == False:
            messages.error(request, 'Username/Password must be at least 4 characters long. And Username should only contain alphanumeric characters.')
            return render(request, "home/home.html")

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, "home/home.html")

        # Check if the username or email already exists
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.error(request, 'Username/Email already exists.')
            return render(request, "home/home.html")

        # Create the new user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Automatically log the user in after successful registration
        login(request, user)
        messages.success(request, f'Welcome, {user.username}! You have successfully Signed up.')

        # Get the next parameter from the request, if available
        next_url = request.POST.get('next', '/')
        return redirect(next_url)
    else:
        messages.error(request, '404 - Not Found')
        return render(request, "home/home.html")

# SignIn View
def signin(request):
    if request.method == 'POST':
        username_or_email = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username_or_email)  # First try to find by username
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username_or_email)  # If not found by username, try to find by email
            except User.DoesNotExist:
                messages.error(request, 'Invalid username/email or password.')
                return render(request, "home/home.html")

        # Authenticate the user with the found user object
        user = authenticate(request, username=user.username, password=password)
        if user is not None:
            login(request, user)
            # Get the next parameter from the request, if available
            next_url = request.POST.get('next', '/')
            return redirect(next_url)  # Redirect to the intended page (room or home)
        else:
            messages.error(request, 'Invalid Credentials.')
            return render(request, "home/home.html")
    else:
        messages.error(request, '404 - Not Found')
        return render(request, "home/home.html")

# SignOut View
def signout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been successfully logged out.')
    return render(request, "home/home.html")