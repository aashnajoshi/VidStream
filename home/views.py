from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Contact

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
        contact = Contact(name=user_name, email=user_email, message=user_message, file_path=attachment)
        
        # Validate form data
        if len(user_name) < 2 or len(user_email) < 3 or len(user_message) < 4:
            messages.error(request, 'Invalid form data!')
            return redirect('contact')
        else:
            contact.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        return render(request, 'home/contact.html', context={'title': 'Contact'})

# Search View
def search(request):
    query = request.GET.get('query')
    if len(query) > 78:
        allPosts = []
    else:
        allPostsTitle = [post.title for post in Post.objects.all()]
        allPostsContent = [post.content for post in Post.objects.all()]
        allPosts = [post for post in Post.objects.all() if query in post.title or query in post.content]
    if len(allPosts) == 0:
        messages.warning(request, f'No search results found for "{query}". Please refine your query.')

    return render(request, 'home/search.html', context={'title': 'Search', 'allPosts': allPosts, 'query': query})

# Signup View
def signup(request):
    if request.method == 'POST':
        user_email = request.POST.get('email')
        user_password = request.POST.get('password')

        if len(user_email) < 3 or len(user_password) < 4:
            messages.error(request, 'Invalid form data!')
            return redirect('signup')

        # Check if email already exists
        if User.objects.filter(username=user_email).exists():
            messages.error(request, 'Email already in use!')
            return redirect('signup')

        # Create new user
        user = User.objects.create_user(username=user_email, password=user_password)
        user.save()

        messages.success(request, 'Your account has been created successfully!')
        return redirect('signin')

    else:
        return render(request, 'home/home.html', context={'title': 'Home'})
        
# Signin View
def signin(request):
    if request.method == 'POST':
        user_email = request.POST.get('email')
        user_password = request.POST.get('password')

        user = authenticate(username=user_email, password=user_password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials!')
            return redirect('signin')
    else:
        return render(request, 'home/home.html', context={'title': 'Home'})