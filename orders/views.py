import sys
from rest_framework.decorators import api_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from storage.models import Storage

from .models import Order, OrderStorage

# Swagger documentation for the index view
@swagger_auto_schema(
    method='GET',
    operation_description="Retrieve a list of orders with total prices.",
    responses={
        200: openapi.Response(description="List of orders with total prices"),
    }
)
@login_required
@api_view(['GET'])
def index(request):
    user = request.user
    if user.is_staff:
        # User is staff, show all orders
        orders = Order.objects.all()
    else:
        # User is not staff, show their own orders
        orders = Order.objects.filter(user=user)

    for order in orders:
        total_price = 0
        order_storages = order.orderstorage_set.select_related('storage')
        for order_storage in order_storages:
            total_price += order_storage.storage.price * order_storage.quantity
        order.total_price = total_price
    
    return render(request, 'orders/index.html', {'orders': orders})


# Swagger documentation for the add view
@swagger_auto_schema(
    methods=['GET', 'POST'],
    operation_description="Create a new order with associated storage items.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'city': openapi.Schema(type=openapi.TYPE_STRING),
            'location': openapi.Schema(type=openapi.TYPE_STRING),
            'date': openapi.Schema(type=openapi.TYPE_STRING, format='date-time'),
            'guests': openapi.Schema(type=openapi.TYPE_INTEGER),
            'type': openapi.Schema(type=openapi.TYPE_INTEGER),
            'storage_data': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.TYPE_INTEGER),
            'quantities': openapi.Schema(type=openapi.TYPE_OBJECT, additional_properties=openapi.Schema(type=openapi.TYPE_INTEGER)),
        },
        required=['city', 'location', 'date', 'guests', 'type', 'storage_data', 'quantities']
    ),
    responses={
        200: "Order created successfully",
        400: "Bad request data",
    }
)
@login_required
@api_view(['GET', 'POST'])
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

# Swagger documentation for the approve view
@swagger_auto_schema(
    method='POST',
    operation_description="Approve an order.",
    responses={
        200: "Order approved successfully",
        400: "Bad request data",
    }
)
@login_required
@api_view(['POST'])
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

# Swagger documentation for the decline view
@swagger_auto_schema(
    method='POST',
    operation_description="Decline an order.",
    responses={
        200: "Order declined successfully",
        400: "Bad request data",
    }
)
@login_required
@api_view(['POST'])
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

# Swagger documentation for the whitdraw view
@swagger_auto_schema(
    method='POST',
    operation_description="Withdraw an order.",
    responses={
        200: "Order withdrawn successfully",
        400: "Bad request data",
    }
)
@login_required
@api_view(['POST'])
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

# Swagger documentation for the complete view
@swagger_auto_schema(
    method='POST',
    operation_description="Mark an order as complete.",
    responses={
        200: "Order marked as complete successfully",
        400: "Bad request data",
    }
)
@login_required
@api_view(['POST'])
def complete(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        if order.status == 2:  # Only update status if it's already accepted
            order.status = 5  # Update status to 'Complete' (adjust status code as needed)
            order.save()
    except Order.DoesNotExist:
        pass  # Handle if the order doesn't exist

    return redirect('orders')  # Redirect to the list of orders

# Swagger documentation for the process_payment view
@swagger_auto_schema(
    method='POST',
    operation_description="Process payment for an order.",
    responses={
        200: "Payment processed successfully",
        400: "Invalid input data",
        404: "Order not found",
        409: "Order status does not allow payment processing",
    }
)
@login_required
@api_view(['POST'])
def process_payment(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        if order.status == 5:  # Only update status if it's already accepted
            order.status = 6  # Update status to 'Complete' (adjust status code as needed)
            order.save()
    except Order.DoesNotExist:
        pass  # Handle if the order doesn't exist

    return redirect('orders')  # Redirect to the list of orders

# Swagger documentation for the pay view
@swagger_auto_schema(
    method='GET',
    operation_description="Get payment information for an order.",
    responses={
        200: "Payment information retrieved successfully",
        404: "Order not found",
    }
)
@login_required
@api_view(['GET'])
def pay(request, order_id):
    user = request.user
    orders = Order.objects.filter(id=order_id)

    return render(request, 'orders/payment.html', {'orders': orders})

# Swagger documentation for the order_detail view
@swagger_auto_schema(
    method='GET',
    operation_description="Get details of an order.",
    responses={
        200: "Order details retrieved successfully",
        404: "Order not found",
    }
)
@login_required
@api_view(['GET'])
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_storage_items = order.orderstorage_set.all().prefetch_related('storage')

    orders = Order.objects.exclude(id=order_id)  # Get all orders except the current order

    for order_storage in order_storage_items:
        total_used_quantity = 0
        for other_order in orders:
            for storage_item in other_order.orderstorage_set.all():
                if storage_item.storage.id == order_storage.storage.id:
                    total_used_quantity += storage_item.quantity
        remaining_quantity = int(order_storage.storage.quantity) - total_used_quantity
        order_storage.remaining_quantity = remaining_quantity if remaining_quantity >= 0 else 0
    
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'order_storage_items': order_storage_items
    })