import sys
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


@login_required
def edit(request, storage_id):
    storage = Storage.objects.filter(id=storage_id)

    return render(request, 'storage/edit.html', {'storage': storage})


@login_required
def edit_storage(request, storage_id):
    storage = Storage.objects.get(id=storage_id)
    if request.method == 'POST':
        # Handle editing an existing storage item
        storage.name = request.POST['name']
        storage.quantity = request.POST['quantity']
        storage.price = float(request.POST['price'])
        storage.type = int(request.POST['type'])
        storage.status = int(request.POST['status'])
        storage.save()
        
        return redirect('edit', storage_id=storage_id)  # Correct redirection
    
    return render(request, 'storage/edit.html', {'storage': storage})