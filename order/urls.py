from django.urls import path
from django.shortcuts import render
from .views import OrderSingleProductView, OrderFromCartView, verify

urlpatterns = [
    path('order/product/<int:pk>/', OrderSingleProductView.as_view(), name='order_single_product'),
    path('order/cart/', OrderFromCartView.as_view(), name='order_from_cart'),
    path('order/success/', lambda request: render(request, 'order/order_success.html'), name='order_success'),
    path('payment/verify/', verify, name='verify_payment')
]
