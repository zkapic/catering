from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.models import User

@api_view(['GET'])  # Specify the HTTP methods for the view
@swagger_auto_schema(
    responses={
        200: openapi.Response(
            description="List of users",
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'username': openapi.Schema(type=openapi.TYPE_STRING),
                        # Add more properties here
                    }
                )
            )
        ),
        500: "Internal server error",
    }
)
# Create your views here
def index(request):
    users = User.objects.all()
    return render(request, 'users/index.html', {'users': users})