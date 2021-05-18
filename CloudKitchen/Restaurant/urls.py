from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="Home"),
    path('contact/', views.contact, name="Contact"),
    path('about/', views.about, name="About"),
    path('viewProfile/', views.viewProfile, name="ViewProfile"),
    path('resetPassword/', views.resetPassword, name="ResetPassword"),
    path('updateProfile/', views.updateProfile, name="UpdateProfile"),
    path('open/<str:image>', views.download_image, name="DownloadImage"),
    path('logout/', views.logout, name="LogOut"),
    path('menu/', views.menu, name="Menu"),
    path('addCategory/', views.addCategory, name="AddCategory"),
    path('addCategoryItem/', views.addCategoryItem, name="AddCategoryItem"),
    path('addItem/<str:category>', views.addItem, name="AddItem"),
    path('deleteCategory/<str:category>', views.deleteCategory, name="DeleteCategory"),
    path('deleteItem/<str:category>/<str:item>', views.deleteItem, name="DeleteItem"),
    path('updateCategory/<str:category>', views.updateCategory, name="UpdateCategory"),
    path('updateItem/<str:category>/<str:item>', views.updateItem, name="UpdateItem"),
    path('order/', views.order, name="Order"),
    path('updateOrder/', views.updateOrder, name="UpdateOrder"),
    path('orderHistory/', views.orderHistory, name="OrderHistory"),
]