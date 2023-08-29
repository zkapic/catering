import sys
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.decorators import login_required
from .models import Storage

# Swagger documentation for the index view
@swagger_auto_schema(
    method='GET',
    operation_description="Get a list of storage items.",
    responses={
        200: openapi.Response(
            description="List of storage items",
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'name': openapi.Schema(type=openapi.TYPE_STRING),
                        'quantity': openapi.Schema(type=openapi.TYPE_STRING),
                        'price': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'type': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'status': openapi.Schema(type=openapi.TYPE_INTEGER),
                    }
                )
            ),
        ),
    }
)
@api_view(['GET'])
def index(request):
    storage = Storage.objects.all()
    return render(request, 'storage/index.html', {'storage': storage})

# Swagger documentation for the add view
@swagger_auto_schema(
    method='POST',
    operation_description="Add a new storage item.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'quantity': openapi.Schema(type=openapi.TYPE_STRING),
            'price': openapi.Schema(type=openapi.TYPE_NUMBER),
            'type': openapi.Schema(type=openapi.TYPE_INTEGER),
            'status': openapi.Schema(type=openapi.TYPE_INTEGER),
        },
        required=['name', 'quantity', 'price', 'type', 'status']
    ),
    responses={
        200: "Successfully added the storage item.",
        400: "Bad request data",
    }
)
@login_required
@api_view(['GET', 'POST'])
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


# Swagger documentation for the edit view
@swagger_auto_schema(
    method='GET',
    operation_description="Render the edit storage item form.",
    responses={
        200: openapi.Response(description="Render the edit form"),
    }
)
@login_required
@api_view(['GET'])
def edit(request, storage_id):
    storage = Storage.objects.filter(id=storage_id)

    return render(request, 'storage/edit.html', {'storage': storage})


# Swagger documentation for the edit_storage view
@swagger_auto_schema(
    method='POST',
    operation_description="Edit an existing storage item.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'quantity': openapi.Schema(type=openapi.TYPE_STRING),
            'price': openapi.Schema(type=openapi.TYPE_NUMBER),
            'type': openapi.Schema(type=openapi.TYPE_INTEGER),
            'status': openapi.Schema(type=openapi.TYPE_INTEGER),
        },
        required=['name', 'quantity', 'price', 'type', 'status']
    ),
    responses={
        200: "Successfully edited the storage item.",
        400: "Bad request data",
    }
)
@login_required
@api_view(['POST'])
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

# Swagger documentation for the delete_storage view
@swagger_auto_schema(
    method='DELETE',
    operation_description="Delete an existing storage item.",
    responses={
        204: "Successfully deleted the storage item.",
    }
)
@login_required
@api_view(['DELETE'])
def delete_storage(request, storage_id):
    storage = Storage.objects.get(id=storage_id)
    
    storage.delete()
    return redirect('storage')
