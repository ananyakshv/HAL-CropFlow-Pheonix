from django.contrib import admin
from .models import Crop, FarmerProfile

# Customizing the display of Crop in the admin panel
class CropAdmin(admin.ModelAdmin):
    list_display = ('crop_name', 'farmer_name', 'state', 'city', 'quantity_to_sell', 'price_per_kg', 'available_quantity')
    search_fields = ('crop_name', 'farmer_name', 'state', 'city')
    list_filter = ('state', 'city')

# Customizing the display of FarmerProfile in the admin panel
class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact_number', 'state', 'city', 'created_at')
    search_fields = ('user__username', 'state', 'city')

# Registering the models with customizations
admin.site.register(Crop, CropAdmin)
admin.site.register(FarmerProfile, FarmerProfileAdmin)
