from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser, CustomerProfile
from store.models import Product

# ----------------------------
# Custom User Registration Form
# ----------------------------
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'})
    )
    phone_number = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'})
    )
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'})
    )
    profile_image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        label='Profile Picture'
    )
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tell us about yourself'}),
        label='Bio'
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'profile_image', 'bio', 'password1', 'password2']

# ----------------------------
# Custom User Login Form
# ----------------------------
class CustomUserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
    )

# ----------------------------
# Custom User Profile Update Form
# ----------------------------
class CustomUserProfileUpdateForm(forms.ModelForm):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    phone_number = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    profile_image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        label='Profile Picture'
    )
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label='Bio'
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'profile_image', 'bio']

# ----------------------------
# Custom User Change Form
# ----------------------------
# This is required for imports in views.py
class CustomUserChangeForm(CustomUserProfileUpdateForm):
    class Meta(CustomUserProfileUpdateForm.Meta):
        pass

# ----------------------------
# Customer Profile Form (additional profile info)
# ----------------------------
class CustomerProfileForm(forms.ModelForm):
    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter your address'}),
        label='Address'
    )

    class Meta:
        model = CustomerProfile
        fields = ['address']

# ----------------------------
# Order Cancellation Form (Unorder)
# ----------------------------
class OrderCancelForm(forms.Form):
    reason = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Reason for cancelling your order'}),
        label='Cancellation Reason'
    )


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    

from .models import CustomerProfile  # make sure this model exists

class CustomerProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

    class Meta:
        model = CustomerProfile
        fields = ['first_name', 'last_name', 'email', 'profile_picture']
