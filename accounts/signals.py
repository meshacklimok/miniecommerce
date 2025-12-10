from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, CustomerProfile

@receiver(post_save, sender=CustomUser)
def create_or_update_customer_profile(sender, instance, created, **kwargs):
    # Always use get_or_create to avoid duplicates
    profile, created_profile = CustomerProfile.objects.get_or_create(user=instance)
    
    # Optional: update profile fields if needed
    profile.save()