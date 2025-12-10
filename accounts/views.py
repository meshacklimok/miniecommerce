from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import (
    PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .forms import (
    CustomUserCreationForm, 
    CustomerProfileUpdateForm
)
from .models import CustomUser, CustomerProfile, Order, Wishlist
from store.models import Product
 
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Profile auto-created via signal
            messages.success(request, "Account created successfully!")
            return redirect('accounts:login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


# ----------------------------
# Login / Logout
# ----------------------------
class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

def user_login(request):
    if request.user.is_authenticated:
        return redirect('accounts:customer_dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.GET.get('next') or 'accounts:customer_dashboard'
            return redirect(next_url)
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('accounts:login')


# ----------------------------
# Customer Dashboard
# ----------------------------
@login_required
def customer_dashboard(request):
    user = request.user
    profile, _ = CustomerProfile.objects.get_or_create(user=user)
    orders = Order.objects.filter(customer=user).order_by('-created_at')
    wishlist = Wishlist.objects.filter(customer=user)
    products = Product.objects.filter(quantity__gt=0)  # in stock
    return render(request, 'accounts/customer_dashboard.html', {
        'user': user,
        'profile': profile,
        'orders': orders,
        'wishlist': wishlist,
        'products': products
    })


# ----------------------------
# Profile Update
# ----------------------------
@login_required
def update_customer_profile(request):
    profile, _ = CustomerProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = CustomerProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('accounts:customer_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomerProfileUpdateForm(instance=profile)
    return render(request, 'accounts/update_customer_profile.html', {'form': form})


# ----------------------------
# Order Management
# ----------------------------
@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    if order.status == 'pending':
        order.status = 'cancelled'
        order.save()
        messages.success(request, f"Order #{order.id} cancelled.")
    else:
        messages.error(request, "You cannot cancel this order.")
    return redirect('accounts:customer_dashboard')


@login_required
def order_history(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'accounts/order_history.html', {'orders': orders})


# ----------------------------
# Password Change / Reset
# ----------------------------
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('accounts:password_change_done')

class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'

class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
