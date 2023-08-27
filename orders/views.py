from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Order

@login_required
def index(request):
    user = request.user
    if user.is_staff:
        # User is staff, show all orders
        orders = Order.objects.all()
    else:
        # User is not staff, show their own orders
        orders = Order.objects.filter(user=user)
    
    return render(request, 'orders/index.html', {'orders': orders})

@login_required
def add(request):
    if request.method == 'POST':
        city = request.POST['city']
        location = request.POST['location']
        date = request.POST['date']
        guests = request.POST['guests']
        type = int(request.POST['type'])
        status = 1
        user = request.user

        Order.objects.create(
            city=city,
            location=location,
            date=date,
            guests=guests,
            status=status,
            user = user,
            type = type
        )

        return redirect('orders')  # Redirect to the list of storage items
    
    return render(request, 'orders/add.html')