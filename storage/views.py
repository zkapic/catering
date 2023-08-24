from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Storage

def index(request):
    storage = Storage.objects.all()
    return render(request, 'storage/index.html', {'storage': storage})

@login_required
def add(request):
    if request.method == 'POST':
        name = request.POST['name']
        quantity = request.POST['quantity']
        price = float(request.POST['price'])
        type = int(request.POST['type'])
        status = int(request.POST['status'])

        Storage.objects.create(
            name=name,
            quantity=quantity,
            price=price,
            type=type,
            status=status
        )

        return redirect('storage')  # Redirect to the list of storage items
    
    return render(request, 'storage/add.html')