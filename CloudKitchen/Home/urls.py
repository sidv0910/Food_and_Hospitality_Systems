from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.homepage, name="Home"),
    path('contact/', views.contact, name="ContactUs"),
    path('about/', views.about, name="About"),
    path('partner/', views.partner, name="Partner"),
    path('register/', views.register, name="Register"),
    path('login/', views.login, name="Login"),
    path('forgot/', views.forgot, name="Forgot"),
    path('verify/', views.verify, name="Verify"),
    path('reset/', views.reset, name="Reset"),
    path('user/', include('User.urls')),
    path('restaurantLogin/', views.restaurantLogin, name="RestaurantLogin"),
    path('restaurantForgot/', views.restaurantForgot, name="RestaurantForgot"),
    path('restaurantVerify/', views.restaurantVerify, name="RestaurantVerify"),
    path('restaurantReset/', views.restaurantReset, name="RestaurantReset"),
    path('restaurant/', include('Restaurant.urls')),
    path('deliveryLogin/', views.deliveryLogin, name="DeliveryLogin"),
    path('deliveryForgot/', views.deliveryForgot, name="DeliveryForgot"),
    path('deliveryVerify/', views.deliveryVerify, name="DeliveryVerify"),
    path('deliveryReset/', views.deliveryReset, name="DeliveryReset"),
    path('delivery/', include('Delivery.urls')),
    path('browseRestaurants/', views.browseRestaurant, name="BrowseRestaurants"),
    path('browseRestaurants/<str:id>', views.restaurantMenu, name="RestaurantMenu"),
]