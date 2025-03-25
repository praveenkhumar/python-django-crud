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

@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/product_form.html', {'form': form})

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('product_list')
    return render(request, 'store/product_confirm_delete.html', {'product': product})

# Order CRUD
@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'store/order_list.html', {'orders': orders})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})

@login_required
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            messages.success(request, 'Order created successfully.')
            return redirect('order_detail', pk=order.pk)
    else:
        form = OrderForm()
    return render(request, 'store/order_form.html', {'form': form})

@login_required
def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order updated successfully.')
            return redirect('order_detail', pk=order.pk)
    else:
        form = OrderForm(instance=order)
    return render(request, 'store/order_form.html', {'form': form})

@login_required
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Order deleted successfully.')
        return redirect('order_list')
    return render(request, 'store/order_confirm_delete.html', {'order': order})

# Order Item CRUD
@login_required
def add_to_order(request, order_pk):
    order = get_object_or_404(Order, pk=order_pk, user=request.user)
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            order_item = form.save(commit=False)
            order_item.order = order
            product = order_item.product
            order_item.price = product.price
            order_item.save()
            messages.success(request, f'{product.name} added to your order.')
            return redirect('order_detail', pk=order.pk)
    else:
        form = OrderItemForm()
    return render(request, 'store/add_to_order.html', {'form': form, 'order': order})

@login_required
def update_order_item(request, pk):
    order_item = get_object_or_404(OrderItem, pk=pk, order__user=request.user)
    if request.method == 'POST':
        form = OrderItemForm(request.POST, instance=order_item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order item updated successfully.')
            return redirect('order_detail', pk=order_item.order.pk)
    else:
        form = OrderItemForm(instance=order_item)
    return render(request, 'store/update_order_item.html', {'form': form, 'order_item': order_item})

@login_required
def delete_order_item(request, pk):
    order_item = get_object_or_404(OrderItem, pk=pk, order__user=request.user)
    order_pk = order_item.order.pk
    if request.method == 'POST':
        order_item.delete()
        messages.success(request, 'Item removed from order.')
        return redirect('order_detail', pk=order_pk)
    return render(request, 'store/delete_order_item.html', {'order_item': order_item})