from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class FarmerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='farmer_profile')
    contact_number = models.CharField(max_length=15)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username


from django.db import models

class Crop(models.Model):
    farmer_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50, default='Unknown')
    crop_name = models.CharField(max_length=100)
    quantity_to_sell = models.IntegerField()
    seeds_cost = models.DecimalField(max_digits=10, decimal_places=2)
    fertilizer_cost = models.DecimalField(max_digits=10, decimal_places=2)
    pesticide_cost = models.DecimalField(max_digits=10, decimal_places=2)
    machinery_cost = models.DecimalField(max_digits=10, decimal_places=2)
    labor_cost = models.DecimalField(max_digits=10, decimal_places=2)
    msp = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Add this
    available_quantity = models.IntegerField(default=0)  # New field for tracking quantity available after sales

    def __str__(self):
        return self.crop_name


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    contact_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)  # Optional, for delivery purposes
    created_at = models.DateTimeField(default=timezone.now)  # Example

    def __str__(self):
        return self.user.username



class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    is_checked_out = models.BooleanField(default=False)
    checkout_method = models.CharField(max_length=50, choices=[('meet_farmer', 'Meet Farmer'), ('online_payment', 'Online Payment')], null=True, blank=True)

    def __str__(self):
        return f"Cart for {self.customer.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    quantity_requested = models.PositiveIntegerField()
    total_price = models.FloatField()

    def __str__(self):
        return f"{self.quantity_requested} kg of {self.crop.crop_name} in cart for {self.cart.customer.username}"