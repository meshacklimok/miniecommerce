from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q, F
from .models import Product, Category, ProductImage, Order, OrderItem, OrderTracking
from accounts.models import Wishlist
from .forms import ProductForm, CategoryForm

# ----------------------------
# Helper: check if user is admin
# ----------------------------
def is_admin(user):
    return user.is_superuser

# ----------------------------
# Home Page
# ----------------------------
def home(request):
    products = Product.objects.filter(quantity__gt=0)[:10]  # first 10 featured products
    return render(request, 'store/home.html', {'products': products})

# ----------------------------
# Product List (Customer view)
# ----------------------------
def product_list(request):
    query = request.GET.get('q', '')
    category_filter = request.GET.get('category', '')

    products = Product.objects.filter(quantity__gt=0)

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if category_filter:
        products = products.filter(category__name__icontains=category_filter)

    categories = Category.objects.all()
    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'query': query,
        'category_filter': category_filter
    })

# ----------------------------
# Product Detail
# ----------------------------
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Increment views_count atomically
    Product.objects.filter(id=product.id).update(views_count=F('views_count') + 1)
    product.refresh_from_db(fields=['views_count'])

    # Get all additional images
    additional_images = product.additional_images.all()

    return render(request, 'store/product_detail.html', {
        'product': product,
        'additional_images': additional_images
    })

# ----------------------------
# Admin: Add Product
# ----------------------------
@login_required
@user_passes_test(is_admin)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            files = request.FILES.getlist('additional_images')
            for f in files:
                ProductImage.objects.create(product=product, image=f)
            messages.success(request, f"Product '{product.name}' added successfully.")
            return redirect('store:product_list')
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})

# ----------------------------
# Admin: Update Product
# ----------------------------
@login_required
@user_passes_test(is_admin)
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            files = request.FILES.getlist('additional_images')
            for f in files:
                ProductImage.objects.create(product=product, image=f)
            messages.success(request, f"Product '{product.name}' updated successfully.")
            return redirect('store:product_detail', product_id=product.id)
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/update_product.html', {'form': form, 'product': product})

# ----------------------------
# Admin: Delete Product
# ----------------------------
@login_required
@user_passes_test(is_admin)
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, f"Product '{product.name}' deleted successfully.")
    return redirect('store:product_list')

# ----------------------------
# Wishlist: Add/Remove
# ----------------------------
@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item = Wishlist.objects.filter(customer=request.user, product=product)
    if wishlist_item.exists():
        wishlist_item.delete()
        messages.info(request, f"Removed '{product.name}' from wishlist.")
    else:
        Wishlist.objects.create(customer=request.user, product=product)
        messages.success(request, f"Added '{product.name}' to wishlist.")
    return redirect('store:product_detail', product_id=product.id)

# ----------------------------
# Cart / Add to Cart
# ----------------------------
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order, created = Order.objects.get_or_create(user=request.user, status='pending')
    item, created = OrderItem.objects.get_or_create(order=order, product=product, defaults={'price': product.price, 'quantity': 1})
    if not created:
        item.quantity += 1
        item.save()
    return redirect('store:cart')

@login_required
def cart(request):
    order = Order.objects.filter(user=request.user, status='pending').first()
    items = order.items.all() if order else []
    total = sum(item.get_total_price() for item in items) if order else 0
    return render(request, 'store/cart.html', {'items': items, 'total': total})

# ----------------------------
# Checkout / MPESA Payment
# ----------------------------
@login_required
def checkout(request):
    order = Order.objects.filter(user=request.user, status='pending').first()
    if not order:
        return redirect('store:product_list')

    order.total_amount = sum(item.get_total_price() for item in order.items.all())
    order.save()

    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        if not phone_number:
            return render(request, 'mpesapayment/mpesa_payment.html', {
                "order": order,
                "error": "Please enter a valid phone number."
            })

        # Reduce stock
        for item in order.items.all():
            item.product.quantity -= item.quantity
            item.product.save()

        # Complete order
        order.status = 'completed'
        order.save()

        mpesa_details = {
            "phone_number": phone_number,
            "amount": order.total_amount,
            "account_reference": f"Order #{order.id}",
            "transaction_desc": f"Payment for Order #{order.id}",
        }

        return render(request, 'mpesapayment/mpesa_payment.html', {
            "order": order,
            "mpesa": mpesa_details,
            "success": True
        })

    return render(request, 'mpesapayment/mpesa_payment.html', {"order": order})

# ----------------------------
# Cancel Order
# ----------------------------
@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status == 'pending':
        order.status = 'cancelled'
        order.save()
    return redirect('accounts:customer_dashboard')

# ----------------------------
# Order Detail / Tracking
# ----------------------------
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.items.all()
    tracking_updates = order.tracking_updates.all() if hasattr(order, 'tracking_updates') else []

    # Progress logic for template
    status_order = ['pending', 'processing', 'shipped', 'completed', 'cancelled']
    progress_index = status_order.index(order.status) + 1 if order.status in status_order else 0

    return render(request, 'store/order_detail.html', {
        'order': order,
        'items': items,
        'tracking_updates': tracking_updates,
        'progress_index': progress_index,
        'status_order': status_order,
    })
    
    
def shipping_info(request):
    return render(request, 'store/shipping_info.html')

def about(request):
    return render(request, 'store/about.html')


def contact(request):
    return render(request, 'store/about.html')
