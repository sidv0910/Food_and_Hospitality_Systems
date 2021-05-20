from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.homepage, name="UserHome"),
    path('contact/', views.contact, name="UserContact"),
    path('about/', views.about, name="UserAbout"),
    path('logout/', views.logout, name="UserLogout"),
    path('profile/', views.viewProfile, name="UserProfile"),
    path('resetPassword/', views.resetPassword, name="UserResetPassword"),
    path('updateProfile/', views.updateProfile, name="UserUpdateProfile"),
    path('browseRestaurant/', views.browseRestaurant, name="UserBrowseRestaurant"),
    path('browseRestaurant/<str:id>', views.restaurantMenu, name="UserRestaurantMenu"),
    path('addToCart/', views.addToCart, name="AddToCart"),
    path('removeFromCart/<str:restaurant>/<str:category>/<str:item>', views.removeFromCart, name="RemoveFromCart"),
    path('cart/', views.viewCart, name="ViewCart"),
    path('updateCart/', views.updateCart, name="UpdateCart"),
    path('deleteFromCart/<str:restaurant>/<str:category>/<str:item>', views.deleteFromCart, name="DeleteFromCart"),
    path('proceed/', views.proceed, name="Proceed"),
    path('final/', views.final, name="Final"),
    path('saveAndFinal/', views.saveAndFinal, name="SaveAndFinal"),
    path('order/', views.order, name="UserOrder"),
    path('orderHistory/', views.orderHistory, name="UserOrderHistory"),
    path('submitFeedback/<str:id>', views.submitFeedback, name="SubmitFeedback"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)