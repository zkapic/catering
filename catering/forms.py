from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()  # Use the appropriate User model
        fields = ['username', 'email', 'password1', 'password2']