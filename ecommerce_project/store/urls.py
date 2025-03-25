# store/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Product URLs
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/new/', views.product_create, name='product_create'),
    path('products/<int:pk>/edit/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    
    # Order URLs
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/new/', views.order_create, name='order_create'),
    path('orders/<int:pk>/edit/', views.order_update, name='order_update'),
    path('orders/<int:pk>/delete/', views.order_delete, name='order_delete'),
    
    # Order Item URLs
    path('orders/<int:order_pk>/add-item/', views.add_to_order, name='add_to_order'),
    path('order-items/<int:pk>/edit/', views.update_order_item, name='update_order_item'),
    path('order-items/<int:pk>/delete/', views.delete_order_item, name='delete_order_item'),
]