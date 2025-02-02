from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CropInputForm
from .models import Crop
from django.contrib.auth.forms import AuthenticationForm
from .models import FarmerProfile
from .models import Cart, Crop, CustomerProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomerSignUpForm, CustomerLoginForm
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render
from .models import Crop
from django.shortcuts import render
from .models import Cart, Crop



def dashboard(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'farmer_profile'):
            return redirect('farmer_dashboard')
        else:
            return redirect('customer_dashboard')
    return redirect('landing_page')


@login_required
def customer_dashboard(request):
    # Get the cart for the logged-in customer
    cart = Cart.objects.filter(customer=request.user, is_checked_out=False).first()

    # Get the total number of distinct crops in the cart
    cart_item_count = 0
    if cart:
        cart_item_count = CartItem.objects.filter(cart=cart).values('crop').distinct().count()

    # Query for crops that have a quantity greater than 0
    crops = Crop.objects.filter(quantity_to_sell__gt=0)  # Only crops with non-zero quantity

    return render(request, 'core/customer_dashboard.html', {
        'cart_item_count': cart_item_count,
        'crops': crops,
    })




from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Signup View
def customer_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            User.objects.create_user(username=username, password=password)
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('customer_login')
        except Exception as e:
            messages.error(request, "Username already exists.")
    return render(request, 'core/customer_signup.html')

# Login View
def customer_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Check if the username exists
        if not User.objects.filter(username=username).exists():
            messages.error(request, "Username not registered")
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('customer_dashboard')
            else:
                messages.error(request, "Incorrect password")

    return render(request, 'core/customer_login.html')

# Logout View
def customer_logout(request):
    logout(request)
    return redirect('customer_login')


def landing_page(request):
    if request.method == "POST":
        user_type = request.POST.get('user_type')
        if user_type == "farmer":
            return redirect('farmer_login')  # Redirect to Farmer login page
        elif user_type == "customer":
            return redirect('customer_login')  # Redirect to Customer login page
    return render(request, 'core/landing_page.html')  # Render the landing page


from decimal import Decimal  # Import Decimal at the top

@login_required(login_url='/farmer/login/')
def farmer_dashboard(request):
    if request.method == 'POST':
        form = CropInputForm(request.POST)
        if form.is_valid():
            # Retrieve and ensure all costs are Decimal
            quantity = form.cleaned_data['quantity']
            seeds_cost = Decimal(form.cleaned_data['seeds_cost'])
            fertilizers_cost = Decimal(form.cleaned_data['fertilizers_cost'])
            pesticides_cost = Decimal(form.cleaned_data['pesticides_cost'])
            machinery_fuel_cost = Decimal(form.cleaned_data['machinery_fuel_cost'])
            family_labor_cost = Decimal(form.cleaned_data['family_labor_cost'])

            # Calculate A2 + FL and MSP
            a2_fl = seeds_cost + fertilizers_cost + pesticides_cost + machinery_fuel_cost + family_labor_cost
            msp = a2_fl * Decimal(1.5)
            price_per_kg = (msp*Decimal(1.5)) / Decimal(quantity)

            # Create a new Crop instance
            crop = Crop(
                crop_name=form.cleaned_data['crop_name'],
                seeds_cost=seeds_cost,
                fertilizer_cost=fertilizers_cost,  # Ensure you match field names
                pesticide_cost=pesticides_cost,
                machinery_cost=machinery_fuel_cost,
                labor_cost=family_labor_cost,
                msp=msp,
                price_per_kg=price_per_kg,  # Save this field
                quantity_to_sell=quantity,
                farmer_name=form.cleaned_data['farmer_name'],
                contact_number=form.cleaned_data['contact_number'],
                state=form.cleaned_data['state'],
                city=form.cleaned_data['city'],
            )
            crop.save()
            return redirect('farmer_dashboard')
    else:
        form = CropInputForm()

    # Fetch all crops to display
    crops = Crop.objects.all()

    return render(request, 'core/farmer_dashboard.html', {'form': form, 'crops': crops})

from django.contrib.auth.models import User  # Import User model

def farmer_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        # Check if username exists
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Username not registered')
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('farmer_dashboard')
            else:
                messages.error(request, 'Invalid password')

    return render(request, 'core/farmer_login.html')

from .models import FarmerProfile

def farmer_signup(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        

        if password == confirm_password:
            try:
                user = User.objects.create_user(username=username, password=password)
                user.save()

                # Create FarmerProfile
                FarmerProfile.objects.create(
                    user=user, 
                    
                )

                messages.success(request, 'Account created successfully!')
                return redirect('farmer_login')
            except Exception as e:
                messages.error(request, f"Error: {e}")
        else:
            messages.error(request, 'Passwords do not match')
    return render(request, 'core/farmer_signup.html')

def farmer_logout(request):
    logout(request)  # Logs out the current user
    return redirect('landing_page')


from django.shortcuts import render, redirect
from .forms import CropForm
from .models import Crop

def add_crop(request):
    if request.method == 'POST':
        form = CropForm(request.POST)
        if form.is_valid():
            # Extract the data from the form
            farmer_name = form.cleaned_data['farmer_name']
            contact_number = form.cleaned_data['contact_number']
            state = form.cleaned_data['state']
            city = form.cleaned_data['city']

            crop_name = form.cleaned_data['crop_name']
            quantity_to_sell = form.cleaned_data['quantity_to_sell']
            seeds_cost = form.cleaned_data['seeds_cost']
            fertilizer_cost = form.cleaned_data['fertilizer_cost']
            pesticide_cost = form.cleaned_data['pesticide_cost']
            machinery_cost = form.cleaned_data['machinery_cost']
            labor_cost = form.cleaned_data['labor_cost']

            # Calculate MSP (multiply by 1.5)
            msp = (seeds_cost + fertilizer_cost + pesticide_cost + machinery_cost + labor_cost) * 1.5

            # Save the crop details and farmer's info into the database (assuming you have a Crop model)
            crop = Crop(
                farmer_name=farmer_name,
                contact_number=contact_number,
                state=state,
                city=city,
                crop_name=crop_name,
                quantity_to_sell=quantity_to_sell,
                seeds_cost=seeds_cost,
                fertilizer_cost=fertilizer_cost,
                pesticide_cost=pesticide_cost,
                machinery_cost=machinery_cost,
                labor_cost=labor_cost,
                msp=msp
            )
            crop.save()

            return redirect('success_page')  # Redirect to a success page or show a success message
    else:
        form = CropForm()

    return render(request, 'core/add_crop.html', {'form': form})


def customer_home(request):
    return render(request, 'core/customer_home.html')

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from core.models import Crop, Cart, CartItem  # Ensure these models are imported

@login_required
def add_to_cart(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id)

    if request.method == 'POST':
        quantity_requested = int(request.POST.get('quantity_requested'))

        # Check if the requested quantity is available
        if quantity_requested <= crop.quantity_to_sell:
            # Get or create the cart for the user
            cart, created = Cart.objects.get_or_create(customer=request.user, is_checked_out=False)

            # Add to cart logic (create or update the CartItem)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                crop=crop,
                defaults={
                    'quantity_requested': quantity_requested,
                    'total_price': quantity_requested * float(crop.price_per_kg)
                }
            )
            if not created:
                cart_item.quantity_requested += quantity_requested
                cart_item.total_price += quantity_requested * float(crop.price_per_kg)
                cart_item.save()

            # Update the crop's available quantity
            crop.quantity_to_sell -= quantity_requested
            crop.save()

            # Debugging prints
            print(f"Crop '{crop.crop_name}' quantity before update: {crop.quantity_to_sell + quantity_requested}")
            print(f"Crop '{crop.crop_name}' quantity after update: {crop.quantity_to_sell}")

            return redirect('customer_dashboard')  # Redirect to the cart page
        else:
            error = "Insufficient quantity available."
            return render(request, 'core/add_to_cart.html', {'crop': crop, 'error': error})

    return render(request, 'core/add_to_cart.html', {'crop': crop})

@login_required
def view_cart(request):
    print("view_cart function executed")  # For debugging
    try:
        cart = Cart.objects.get(customer=request.user, is_checked_out=False)
        cart_items = CartItem.objects.filter(cart=cart)
        total_price = sum(item.total_price for item in cart_items)  # Compute total price
    except Cart.DoesNotExist:
        cart_items = []
        total_price = 0

    return render(request, 'core/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

# In views.py
def thank_you(request):
    return render(request, 'core/thank_you.html')

def checkout(request):
    if request.method == "POST":
        delivery_option = request.POST.get('delivery_option')
        
        # Get the cart items
        cart_items = CartItem.objects.filter(cart__customer=request.user, cart__is_checked_out=False)
        if not cart_items:
            messages.error(request, "Your cart is empty.")
            return redirect('customer_cart')

        total_price = sum(item.total_price for item in cart_items)  # Calculate total price

        # Ensure farmer details are extracted from the cart items
        farmer_details = {
            'name': cart_items[0].crop.farmer_name,
            'phone': cart_items[0].crop.contact_number,
            'city': cart_items[0].crop.city,
            'state': cart_items[0].crop.state,
        }

        if delivery_option == "direct_contact":
            return render(request, 'core/direct_contact.html', {'farmer_details': farmer_details, 'total_price': total_price})
        
        elif delivery_option == "online_payment":
            return render(request, 'core/online_payment.html', {'total_price': total_price, 'farmer_details': farmer_details})
        
        else:
            messages.error(request, "Invalid delivery option selected.")
            return redirect('customer_cart')

    return redirect('customer_dashboard')

from django.shortcuts import render, redirect
from .models import Cart, CartItem

def direct_contact(request):
    # Get the logged-in user's cart
    try:
        cart = Cart.objects.get(customer=request.user, is_checked_out=False)
    except Cart.DoesNotExist:
        return render(request, 'core/direct_contact.html', {'error': 'Your cart is empty.'})

    # Retrieve the first cart item (assuming all items belong to the same farmer)
    cart_item = cart.items.first()
    if not cart_item:
        return render(request, 'core/direct_contact.html', {'error': 'Your cart is empty.'})

    # Get farmer details from the associated crop
    crop = cart_item.crop
    farmer_details = {
        'name': crop.farmer_name,
        'phone': crop.contact_number,
        'city': crop.city,
        'state': crop.state
    }

    return render(request, 'core/direct_contact.html', {'farmer_details': farmer_details})

from django.shortcuts import render
from .models import Cart, CartItem

def online_payment(request):
    try:
        # Get the logged-in user's cart
        cart = Cart.objects.get(customer=request.user, is_checked_out=False)
    except Cart.DoesNotExist:
        return render(request, 'core/online_payment.html', {'error': 'Your cart is empty.'})

    # Retrieve the first cart item (assuming all items are from the same farmer)
    cart_item = cart.items.first()
    if not cart_item:
        return render(request, 'core/online_payment.html', {'error': 'Your cart is empty.'})

    # Get farmer details from the associated crop
    crop = cart_item.crop
    farmer_details = {
        'name': crop.farmer_name,
        'phone': crop.contact_number,
        'city': crop.city,
        'state': crop.state
    }

    return render(request, 'core/online_payment.html', {'farmer_details': farmer_details})

def payment(request, cart_id):
    try:
        cart = get_object_or_404(Cart, id=cart_id, customer=request.user, is_checked_out=True)
        cart_items = cart.items.all()  # Using related_name 'items' from CartItem
        if cart_items.exists():
            farmer_contact_number = cart_items.first().crop.contact_number

            return render(request, 'core/online_payment.html', {
                'farmer_contact_number': farmer_contact_number,
                'cart': cart,
                'cart_items': cart_items
            })
        else:
            return render(request, 'core/checkout.html', {'error': 'Your cart is empty.'})

    except Cart.DoesNotExist:
        return render(request, 'core/checkout.html', {'error': 'Cart not found.'})

def crop_detail(request, crop_id):
    crop = Crop.objects.get(id=crop_id)
    return render(request, 'core/add_to_cart.html', {
        'crop': crop,  # Pass the crop object to the template
    })


from django.shortcuts import redirect
from .models import Cart, CartItem
@login_required
def delete_from_cart(request, cart_item_id):
    try:
        # Get the cart item to be deleted
        cart_item = CartItem.objects.get(id=cart_item_id)
        crop = cart_item.crop

        # Update the crop's available quantity by adding the quantity back
        crop.quantity_to_sell += cart_item.quantity_requested
        crop.save()

        # Debugging prints
        print(f"Crop '{crop.crop_name}' quantity before deletion: {crop.quantity_to_sell - cart_item.quantity_requested}")
        print(f"Crop '{crop.crop_name}' quantity after deletion: {crop.quantity_to_sell}")

        # Delete the cart item
        cart_item.delete()

        # Redirect back to the customer dashboard or cart
        return redirect('customer_dashboard')  # Or 'cart' if you prefer
    except CartItem.DoesNotExist:
        # Handle the case where the cart item does not exist
        return redirect('customer_dashboard')  # Or display an error message

from django.shortcuts import redirect
from django.utils.translation import activate
from django.conf import settings

def set_language_view(request):
    language = request.GET.get('language')
    if language:
        activate(language)  # Activate the selected language
        response = redirect(request.META.get('HTTP_REFERER', '/'))  # Redirect to the previous page or home if no referrer
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)  # Set language cookie
        request.session[settings.LANGUAGE_COOKIE_NAME] = language  # Also store in session
        return response
    else:
        return redirect('/')  # If no language is selected, redirect to homepage
