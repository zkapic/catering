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

@login_required
def approve(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        if order.status == 1:  # Only update status if it's not already approved
            order.status = 2  # Update status to 'Approved' (adjust status code as needed)
            order.save()
    except Order.DoesNotExist:
        pass  # Handle if the order doesn't exist

    return redirect('orders')  # Redirect to the list of orders


@login_required
def decline(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        if order.status == 1:  # Only update status if it's not already approved or declined
            order.status = 3  # Update status to 'Declined' (adjust status code as needed)
            order.save()
    except Order.DoesNotExist:
        pass  # Handle if the order doesn't exist

    return redirect('orders')  # Redirect to the list of orders

@login_required
def whitdraw(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        if order.status == 1:  # Only update status if it's not already approved or declined
            order.status = 4  # Update status to 'Declined' (adjust status code as needed)
            order.save()
    except Order.DoesNotExist:
        pass  # Handle if the order doesn't exist

    return redirect('orders')  # Redirect to the list of orders

@login_required
def complete(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        if order.status == 2:  # Only update status if it's already accepted
            order.status = 5  # Update status to 'Complete' (adjust status code as needed)
            order.save()
    except Order.DoesNotExist:
        pass  # Handle if the order doesn't exist

    return redirect('orders')  # Redirect to the list of orders

@login_required
def process_payment(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        if order.status == 5:  # Only update status if it's already accepted
            order.status = 6  # Update status to 'Complete' (adjust status code as needed)
            order.save()
    except Order.DoesNotExist:
        pass  # Handle if the order doesn't exist

    return redirect('orders')  # Redirect to the list of orders

@login_required
def pay(request, order_id):
    user = request.user
    orders = Order.objects.filter(id=order_id)

    return render(request, 'orders/payment.html', {'orders': orders})