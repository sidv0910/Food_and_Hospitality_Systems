import mimetypes
import os
from wsgiref.util import FileWrapper
from datetime import datetime
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ContactUsForm, UpdateProfileForm
from .models import Query
from Home.models import Delivery
from Restaurant.models import Orders
from Restaurant.forms import ResetPasswordForm

def homepage(request):
    if 'email' in request.session and Delivery.objects.filter(email=request.session['email']).exists():
        obj = Delivery.objects.get(email=request.session['email'])
        return render(request, 'deliveryIndex.html', {'name': obj.name})
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def contact(request):
    if 'email' in request.session and Delivery.objects.filter(email=request.session['email']).exists():
        obj = Delivery.objects.get(email=request.session['email'])
        if request.method == "POST":
            form = ContactUsForm(request.POST)
            if form.is_valid():
                obj = Query()
                obj.name = form.cleaned_data['name']
                obj.email = Delivery.objects.get(email=form.cleaned_data['email'])
                obj.subject = form.cleaned_data['subject']
                obj.message = form.cleaned_data['message']
                obj.save()
                messages.success(request, "Query Sent Successfully.")
                return redirect('/delivery')
            else:
                messages.error(request, "Failed to send query.")
                return redirect('/delivery/contact')
        else:
            form = ContactUsForm()
            form.initial['name'] = obj.name
            form.initial['email'] = obj.email
            return render(request, "deliveryContact.html", {'name': obj.name, 'form': form})
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def about(request):
    if 'email' in request.session and Delivery.objects.filter(email=request.session['email']).exists():
        obj = Delivery.objects.get(email=request.session['email'])
        return render(request, 'deliveryAbout.html', {'name': obj.name})
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def viewProfile(request):
    if 'email' in request.session and Delivery.objects.filter(email=request.session['email']).exists():
        obj = Delivery.objects.get(email=request.session['email'])
        return render(request, 'deliveryProfile.html', {'name': obj.name, 'obj': obj})
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def download_file(request, file):
    if 'email' in request.session and Delivery.objects.filter(email=request.session['email']).exists():
        obj = Delivery.objects.get(email=request.session['email'])
        if file == "rc":
            img = obj.vehicle_registration_certificate
        elif file == "dl":
            img = obj.driving_license
        else:
            return redirect('/delivery/viewProfile')
        wrapper = FileWrapper(open(str(img.file), 'rb'))
        content_type = mimetypes.guess_type(img.name.split('/')[-1])[0]
        response = HttpResponse(wrapper, content_type=content_type)
        response['Content-Length'] = os.path.getsize(str(img.file))
        response['Content-Disposition'] = "attachment; filename=%s" % img.name.split('/')[-1]
        return response
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def resetPassword(request):
    if 'email' in request.session and Delivery.objects.filter(email=request.session['email']).exists():
        obj = Delivery.objects.get(email=request.session['email'])
        if request.method == "POST":
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                old_password = form.cleaned_data['old_password']
                new_password = form.cleaned_data['re_password']
                if old_password != obj.password:
                    messages.error(request, "Wrong old password.\\nTry again!")
                    return redirect('/delivery/resetPassword')
                elif new_password == obj.password:
                    messages.error(request, "New password is same as old password.\\nTry again!")
                    return redirect('/delivery/resetPassword')
                else:
                    obj.password = new_password
                    obj.save()
                    messages.success(request, "Password reset successfully.")
                    return redirect('/delivery/viewProfile')
            else:
                messages.error(request, "Failed to reset password.\\nTry again!")
                return redirect('/delivery/resetPassword')
        else:
            form = ResetPasswordForm()
            return render(request, 'deliveryResetPassword.html', {'name': obj.name, 'form': form})
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def updateProfile(request):
    if 'email' in request.session and Delivery.objects.filter(email=request.session['email']).exists():
        obj = Delivery.objects.get(email=request.session['email'])
        if request.method == "POST":
            form = UpdateProfileForm(request.POST)
            if form.is_valid():
                obj.contact = form.cleaned_data['contact']
                obj.address = form.cleaned_data['address']
                obj.save()
                messages.success(request, "Profile updated successfully.")
                return redirect('/delivery/viewProfile')
            else:
                messages.error(request, "Failed to update profile.\\nTry again!")
                return redirect('/delivery/updatePassword')
        else:
            form = UpdateProfileForm()
            form.initial['contact'] = obj.contact
            form.initial['address'] = obj.address
            return render(request, 'deliveryUpdateProfile.html', {'name': obj.name, 'obj': obj, 'form': form})
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def logout(request):
    request.session.flush()
    request.session.clear_expired()
    messages.success(request, "Logged Out Successfully.")
    return redirect('/')

def order(request):
    if 'email' in request.session and Delivery.objects.filter(email=request.session['email']).exists():
        obj = Delivery.objects.get(email=request.session['email'])
        obj1 = Orders.objects.filter(delivery=obj.delivery_id, delivered=False)
        if obj1.exists():
            items = {}
            for i in obj1:
                items[i.order_number] = [j.strip("'") for j in i.items.strip('[]').split(', ')]
            quantity = {}
            for i in obj1:
                quantity[i.order_number] = [j.strip("'") for j in i.quantity.strip('[]').split(', ')]
            return render(request, 'orderDelivery.html', {'name': obj.name, 'obj': obj1, 'items': items, 'quantity': quantity})
        else:
            obj1 = None
            return render(request, 'orderDelivery.html', {'name': obj.name, 'obj': obj1})
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def mail(request, order_id):
    obj = Orders.objects.get(order_number=order_id)
    subject = "Your order summary for order no. " + str(order_id)
    message = "Thanks for choosing Cloud Kitchen, " + obj.user.name + "! Here are your order details:\n\nOrder No.: " + str(order_id) + "\n\nOrder Status: " + "Delivered" + "\n\nOrder Delivered At: " + obj.date.strftime('%A, %b %d, %Y') + obj.time.strftime('%I:%M %p') + "\n\nOrder From:\n" + obj.restaurant.restaurant_name + "\n" + obj.restaurant.address + "\n" + obj.restaurant.city + " - " + str(obj.restaurant.zip) + "\n\nDelivery To: \n" + obj.user.name + "\n" + obj.address.line1 + "\n" + obj.address.line2 + "\n" + obj.address.landmark + "\n" + obj.address.locality + "\n" + obj.address.city + " - " + str(obj.address.zip) + "\n\nItems: \n"
    items = [j.strip("'") for j in obj.items.strip('[]').split(', ')]
    quantity = [j.strip("'") for j in obj.quantity.strip('[]').split(', ')]
    for i, j in zip(quantity, items):
        message += i + " x " + j + "\n"
    message += "\nThank You,\nCloud Kitchen Team"
    to = [obj.user.email]
    res = send_mail(subject, message, settings.EMAIL_HOST_USER, to)
    if res == 1:
        return True
    else:
        return False

def updateOrder(request):
    if 'email' in request.session and Delivery.objects.filter(email=request.session['email']).exists():
        obj = Delivery.objects.get(email=request.session['email'])
        if request.method == "POST":
            order_id = request.POST['order_id']
            obj1 = Orders.objects.get(order_number=order_id)
            if obj1.picked_up:
                if obj1.out_for_delivery:
                    if obj1.delivered:
                        return redirect('/delivery/order')
                    else:
                        obj1.delivered = True
                        obj1.date = datetime.now().date()
                        obj1.time = datetime.now().time()
                        obj.status = False
                        obj.save()
                        obj1.save()
                        mail(request, obj1.order_number)
                        messages.success(request, "Ordered Delivered Successfully")
                else:
                    obj1.out_for_delivery = True
                    obj1.save()
            else:
                obj1.picked_up = True
                obj1.save()
            return redirect('/delivery/order')
        else:
            return redirect('/delivery/order')
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def orderHistory(request):
    if 'email' in request.session and Delivery.objects.filter(email=request.session['email']).exists():
        obj = Delivery.objects.get(email=request.session['email'])
        obj1 = Orders.objects.filter(delivery=obj.delivery_id, delivered=True)
        if obj1.exists():
            items = {}
            for i in obj1:
                items[i.order_number] = [j.strip("'") for j in i.items.strip('[]').split(', ')]
            quantity = {}
            for i in obj1:
                quantity[i.order_number] = [j.strip("'") for j in i.quantity.strip('[]').split(', ')]
            return render(request, 'orderHistoryDelivery.html', {'name': obj.name, 'obj': obj1, 'items': items, 'quantity': quantity})
        else:
            obj1 = None
            return render(request, 'orderHistoryDelivery.html', {'name': obj.name, 'obj': obj1})
    else:
        messages.error(request, "Please login first.")
        return redirect('/')