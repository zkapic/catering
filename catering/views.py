from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/users')  # Redirect logged-in users to '/users' page
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/users')  # Replace with your desired URL after successful login
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

from .forms import CustomUserCreationForm  # Import your custom form

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after registration
            login(request, user)
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('/users')  # Replace 'users' with the URL to redirect after successful registration
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = CustomUserCreationForm()  # Use the custom form here
    return render(request, 'register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')  # Replace 'home' with the URL you want to redirect to after logout