from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField

# ----------------------------
# Custom User
# ----------------------------
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_image = CloudinaryField('profile_image', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

# ----------------------------
# Customer Profile
# ----------------------------
class CustomerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='customer_profile')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    def __str__(self):
        return f"{self.user.username}'s Profile"

# ----------------------------
# Wishlist
# ----------------------------
class Wishlist(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE, related_name='wishlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('customer', 'product')

    def __str__(self):
        return f"{self.customer.username} likes {self.product.name}"

# ----------------------------
# Cart
# ----------------------------
class Cart(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('customer', 'product')

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.customer.username}'s cart"

# ----------------------------
# Orders & Order Items
# ----------------------------
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    shipping_address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Order {self.id} by {self.customer.username}"

    def calculate_total(self):
        total = sum(item.total_price() for item in self.items.all())
        self.total_amount = total
        self.save()
        return total

    def cancel_order(self):
        if self.status == 'pending':
            self.status = 'cancelled'
            self.save()
            return True
        return False

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='accounts_order')
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def total_price(self):
        return self.quantity * self.price

# ----------------------------
# Signals: Auto-create CustomerProfile
# ----------------------------
@receiver(post_save, sender=CustomUser)
def create_customer_profile(sender, instance, created, **kwargs):
    # Safely create profile if it doesn't exist
    CustomerProfile.objects.get_or_create(user=instance)
