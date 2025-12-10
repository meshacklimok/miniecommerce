from django.db import models
from store.models import Order  # Make sure this is the correct path to your Order model


class MpesaPayment(models.Model):
    """
    Stores M-Pesa STK Push payment attempts.
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,  # Allow null for failed/cancelled payments
        null=True,
        blank=True,
        related_name='mpesa_payments'
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    phone_number = models.CharField(max_length=15)
    mpesa_receipt = models.CharField(max_length=50, blank=True, null=True)
    checkout_request_id = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        help_text="Unique CheckoutRequestID from M-Pesa STK Push"
    )
    response = models.JSONField()  # Store the JSON response from Safaricom
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        order_id = self.order.id if self.order else "N/A"
        return f"MPESA Payment #{self.id} for Order #{order_id}"

