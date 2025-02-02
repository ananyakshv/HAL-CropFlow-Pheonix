from django import forms
from django import forms
from django.contrib.auth.models import User
from django import forms
from .models import Crop
from django.core.validators import RegexValidator


from django import forms

class CropForm(forms.Form):
    # Farmer's details
    farmer_name = forms.CharField(label='Farmer Name', max_length=100)
    contact_number = forms.CharField(label='Contact Number', max_length=15)
    state = forms.CharField(label='State', max_length=50)
    city = forms.CharField(label='City', max_length=50)

    # Crop details
    crop_name = forms.CharField(label='Crop Name', max_length=100)
    quantity_to_sell = forms.IntegerField(label='Quantity to Sell (kg)')
    seeds_cost = forms.DecimalField(label='Total Seeds Cost (₹)', max_digits=10, decimal_places=2)
    fertilizer_cost = forms.DecimalField(label='Total Fertilizer Cost (₹)', max_digits=10, decimal_places=2)
    pesticide_cost = forms.DecimalField(label='Total Pesticide Cost (₹)', max_digits=10, decimal_places=2)
    machinery_cost = forms.DecimalField(label='Machinery/Fuel Cost (₹)', max_digits=10, decimal_places=2)
    labor_cost = forms.DecimalField(label='Family/Unpaid Labor Cost (₹)', max_digits=10, decimal_places=2)


# Define the signup form
class CustomerSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

# Define the login form
class CustomerLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class FarmerSignupForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label="Username",
        widget=forms.TextInput(attrs={'placeholder': 'Enter username'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'})
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Re-enter password'})
    )
    name = forms.CharField(
        max_length=100,
        label="Full Name",
        widget=forms.TextInput(attrs={'placeholder': 'Enter your name'})
    )
    contact_number = forms.CharField(
        max_length=15,
        label="Contact Number",
        widget=forms.TextInput(attrs={'placeholder': 'Enter contact number'})
    )
    state = forms.CharField(
        max_length=50,
        label="State",
        widget=forms.TextInput(attrs={'placeholder': 'Enter state'})
    )
    city = forms.CharField(
        max_length=50,
        label="City",
        widget=forms.TextInput(attrs={'placeholder': 'Enter city'})
    )

from django import forms

class CropInputForm(forms.Form):
    farmer_name = forms.CharField(max_length=100)
    contact_number = forms.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^[0-9]{10}$', 
                message="Please enter a valid 10-digit contact number with no letters or special characters."
            )
        ],
        widget=forms.TextInput(attrs={'maxlength': '10'})
    )    
    state = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50)
    crop_name = forms.CharField(max_length=100)
    quantity = forms.IntegerField()
    seeds_cost = forms.DecimalField(max_digits=10, decimal_places=2)
    fertilizers_cost = forms.DecimalField(max_digits=10, decimal_places=2)
    pesticides_cost = forms.DecimalField(max_digits=10, decimal_places=2)
    machinery_fuel_cost = forms.DecimalField(max_digits=10, decimal_places=2)
    family_labor_cost = forms.DecimalField(max_digits=10, decimal_places=2)


from django import forms
from .models import Cart


class CartForm(forms.Form):
    quantity_requested = forms.IntegerField(
        min_value=1,
        label="Quantity requested",
        help_text="Enter the quantity you want to purchase."
    )

    def __init__(self, *args, **kwargs):
        crop = kwargs.pop('crop', None)
        super().__init__(*args, **kwargs)
        if crop:
            self.fields['quantity_requested'].widget.attrs['max'] = crop.quantity_to_sell
            self.fields['quantity_requested'].help_text = f"Max: {crop.quantity_to_sell} kg"
