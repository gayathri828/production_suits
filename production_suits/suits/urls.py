from django.urls import path
from . import views

urlpatterns = [
    path('customize/', views.suit_customization, name='suit_customization'),
    path('order/', views.place_order, name='place_order'),
    path('orders/confirmation/', views.order_confirmation, name='order_confirmation'),  # New route
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),

]
