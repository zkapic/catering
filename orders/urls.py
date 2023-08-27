from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="orders"),
    path('add/', views.add, name='add_orders'),
]
