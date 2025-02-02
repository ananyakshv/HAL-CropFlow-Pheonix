from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView  # Import LogoutView
from django.conf.urls.i18n import i18n_patterns
from .views import set_language_view  # Import the set_language_view

urlpatterns = [
    # Landing page, can be used as a public entry point
    path('', views.landing_page, name='landing_page'),
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),

    # Farmer related URLs
    path('farmer/', views.farmer_dashboard, name='farmer_dashboard'),
    path('farmer/login/', views.farmer_login, name='farmer_login'),
    path('farmer/signup/', views.farmer_signup, name='farmer_signup'),
    path('farmer/logout/', views.farmer_logout, name='farmer_logout'),
    path('farmer/dashboard/', views.farmer_dashboard, name='farmer_dashboard'),

    # Customer related URLs
    path('customer/', views.customer_dashboard, name='customer_dashboard'),
    path('customer/signup/', views.customer_signup, name='customer_signup'),
    path('customer/login/', views.customer_login, name='customer_login'),
    path('customer/logout/', views.customer_logout, name='customer_logout'),

    path('customer/home/', views.customer_home, name='customer_home'),
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    # Cart URL
    path('add_to_cart/<int:crop_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='cart'),
    path('payment/<int:cart_id>/', views.payment, name='payment'),
    path('cart/delete/<int:cart_item_id>/', views.delete_from_cart, name='delete_from_cart'),

    # Language setting
    path('set_language/', set_language_view, name='set_language'),

    # Checkout and other URLs
    path('checkout/', views.checkout, name='checkout'),
    path('direct-contact/', views.direct_contact, name='direct_contact'),
    path('online-payment/', views.online_payment, name='online_payment'),

    # Default login/logout views from Django
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

