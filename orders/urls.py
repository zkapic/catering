from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="orders"),
    path('add/', views.add, name='add_orders'),
    path('approve/<int:order_id>/', views.approve, name='approve'),
    path('decline/<int:order_id>/', views.decline, name='decline'),
    path('whitdraw/<int:order_id>/', views.whitdraw, name='whitdraw'),
    path('complete/<int:order_id>/', views.complete, name='complete'),
    path('pay/<int:order_id>/', views.pay, name='pay'),
    path('process_payment/<int:order_id>/', views.process_payment, name='process_payment'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
]
