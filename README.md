# Django Crash Course with MySQL CRUD Application

## Part 1: Setup and Basic Concepts

First, let's set up your Django project with MySQL:

```bash
# Install Django and MySQL connector
pip install django mysqlclient

# Create a new Django project
django-admin startproject ecommerce_project
cd ecommerce_project

# Create a new app
python manage.py startapp store
```

Now, let's configure the MySQL database in `settings.py`:

```python
# ecommerce_project/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ecommerce_db',
        'USER': 'root',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Add your app to INSTALLED_APPS
INSTALLED_APPS = [
    # ...
    'store',
]
```

Create your MySQL database:

```sql
CREATE DATABASE ecommerce_db;
```

## Part 2: Define Models

Let's create models for users, products, and orders:

```python
# store/models.py
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.orderitem_set.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    @property
    def subtotal(self):
        return self.price * self.quantity
```

Now create and apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Part 3: Create Views and Forms

Let's create forms for our models:

```python
# store/forms.py
from django import forms
from .models import Product, Order, OrderItem

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
```

Now let's create views for CRUD operations:

```python
# store/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Order, OrderItem
from .forms import ProductForm, OrderForm, OrderItemForm

# Product CRUD
def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product created successfully.')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()
    return render(request, 'store/product_form.html', {'form': form})
```

## Part 4: URLs Configuration

Now let's set up the URL patterns:

```python
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
```

Include these URLs in the main project:

```python
# ecommerce_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('store/', include('store.urls')),
]
```

This completes the setup for a basic Django CRUD application with MySQL integration.
