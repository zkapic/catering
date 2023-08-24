from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User

# Create your views here
def index(request):
    users = User.objects.all()
    return render(request, 'users/index.html', {'users': users})