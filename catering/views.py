from rest_framework.decorators import api_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


from orders.models import Order

@api_view(['POST'])  # Specify the HTTP methods for the view
@swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['username', 'password']
    ),
    responses={
        200: 'Successfully logged in',
        400: 'Invalid input data'
    }
)
def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/home')
        else:
            return redirect('/orders') 
        
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_authenticated:
                if request.user.is_staff:
                    return redirect('/home')
                else:
                    return redirect('/orders')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

from .forms import CustomUserCreationForm  # Import your custom form

@api_view(['POST'])
@swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            # Define properties for your registration request
        },
        required=[
            # List required properties here
        ]
    ),
    responses={
        200: 'Registration successful',
        400: 'Invalid input data'
    }
)
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after registration
            login(request, user)
            messages.success(request, 'Registration successful. You are now logged in.')
            if request.user.is_authenticated:
                if request.user.is_staff:
                    return redirect('/home')
                else:
                    return redirect('/orders')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = CustomUserCreationForm()  # Use the custom form here
    return render(request, 'register.html', {'form': form})

@api_view(['GET'])
@swagger_auto_schema(
    responses={
        200: 'Successfully logged out'
    }
)
def logout_view(request):
    logout(request)
    return redirect('login')  # Replace 'home' with the URL you want to redirect to after logout

@api_view(['GET'])
@swagger_auto_schema(
    responses={
        200: 'Successfully retrieved home view data'
    }
)
@login_required
def home_view(request):
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status=1).count()
    accepted_orders = Order.objects.filter(status=2).count()
    declined_orders = Order.objects.filter(status=3).count()
    completed_orders = Order.objects.filter(status=5).count()

    return render(request, 'dashboard.html', {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'accepted_orders': accepted_orders,
        'declined_orders': declined_orders,
        'completed_orders': completed_orders,
    })
