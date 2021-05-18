from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.homepage, name="DeliveryHome"),
    path('contact/', views.contact, name="DeliveryContact"),
    path('about/', views.about, name="DeliveryAbout"),
    path('viewProfile/', views.viewProfile, name="ViewProfile"),
    path('open/<str:file>', views.download_file, name="DownloadFile"),
    path('resetPassword/', views.resetPassword, name="DeliveryResetPassword"),
    path('updatePassword/', views.updateProfile, name="DeliveryUpdatePassword"),
    path('logout/', views.logout, name="LogOut"),
    path('order/', views.order, name="DeliveryOrder"),
    path('updateOrder/', views.updateOrder, name="DeliveryUpdateOrder"),
    path('orderHistory/', views.orderHistory, name="DeliveryOrderHistory"),
]