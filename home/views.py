import re
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views import View
from django.db.models import Q
from stream.models import Stream
from .models import Contact

# Home View
class HomeView(View):
    def get(self, request):
        return render(request, 'home/home.html', context={'title': 'Home'})

# About View
class AboutView(View):
    def get(self, request):
        return render(request, 'home/about.html', context={'title': 'About'})

# Contact View
class ContactView(View):
    def get(self, request):
        context = {'title': 'Contact'}
        if request.user.is_authenticated:
            context['user_name'] = request.user.username
            context['user_email'] = request.user.email
        return render(request, 'home/contact.html', context)
    
    def post(self, request):
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

# Search View
class SearchView(View):
    def get(self, request):
        query = request.GET.get('query')
        if len(query) > 78:
            allStreams = []
        else:
            allStreams = Stream.objects.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) | 
                Q(genre__icontains=query)
            )

        if not allStreams:
            messages.warning(request, f'No search results found for "{query}". Please refine your query.')
        return render(request, 'home/search.html', context={'title': 'Search', 'allStreams': allStreams, 'query': query})

# SignUp View
class SignUpView(View):
    def get(self, request):
        return render(request, "home/home.html")

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmPassword']

        # Basic form validation
        if len(username) < 4 or len(password) < 4 or not username.isalnum():
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

        # Create the new user and login
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        messages.success(request, f'Welcome, {user.username}! You have successfully signed up.')

        # Get the next parameter from the request, if available
        next_url = request.POST.get('next', '/')
        return redirect(next_url)

# SignIn View
class SignInView(View):
    def get(self, request):
        return render(request, "home/home.html")

    def post(self, request):
        username_or_email = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username_or_email, password=password)
        if user is None:
            # Try to find the user by email if authentication fails
            try:
                user = User.objects.get(email=username_or_email)
                user = authenticate(request, username=user.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            next_url = request.POST.get('next', '/')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username/email or password.')
            return render(request, "home/home.html")

# SignOut View
class SignOutView(View):
    def post(self, request):
        logout(request)
        next_url = request.POST.get('next', request.GET.get('next', '/'))
        return redirect(next_url if next_url.strip() else '/')