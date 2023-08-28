import sys
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from storage.models import Storage

from .models import Order, OrderStorage

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
        selected_storage_data = request.POST.getlist('storage_data')
        quantities = {}  # Dictionary to store storage item quantities
    
        for storage_id in selected_storage_data:
            quantity = request.POST.get(f'quantity_{storage_id}')
            quantities[storage_id] = int(quantity)

        status = 1
        user = request.user

        new_order = Order.objects.create(
            city=city,
            location=location,
            date=date,
            guests=guests,
            status=status,
            user = user,
            type = type
        )

        for storage_id, quantity in quantities.items():
            storage = Storage.objects.get(id=storage_id)
            OrderStorage.objects.create(
                order=new_order,
                storage=storage,
                quantity=quantity
            )


        return redirect('orders')  # Redirect to the list of storage items
    
    storage_items = Storage.objects.all()  # Fetch all storage items from the database
    return render(request, 'orders/add.html', {'storage_items': storage_items})

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

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_storage_items = order.orderstorage_set.all().prefetch_related('storage')
    
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'order_storage_items': order_storage_items
    })