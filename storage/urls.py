from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="storage"),
    path('add/', views.add, name='add_storage'),
    path('edit/<int:storage_id>/', views.edit, name='edit'),
    path('edit_storage/<int:storage_id>/', views.edit_storage, name='edit_storage'),
    path('delete/<int:storage_id>/', views.delete_storage, name='delete_storage'),
]
