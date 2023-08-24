from django.contrib.auth.decorators import login_required
from django.shortcuts import render
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