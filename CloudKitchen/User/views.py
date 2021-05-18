import random
import string

from django.contrib import messages
from django.shortcuts import render, redirect
from datetime import datetime
from .forms import ContactUsForm, UpdateProfileForm, AddressForm
from .models import Query, Address
from Home.models import User, Restaurant, Delivery
from Restaurant.forms import ResetPasswordForm
from Restaurant.models import Category, Item, Orders
from Delivery.models import Cart

def homepage(request):
    if 'email' in request.session and User.objects.filter(email=request.session['email']).exists():
        obj = User.objects.get(email=request.session['email'])
        return render(request, 'userIndex.html', {'name': obj.name, 'count': Cart.objects.filter(user=obj).count()})
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def contact(request):
    if 'email' in request.session and User.objects.filter(email=request.session['email']).exists():
        obj = User.objects.get(email=request.session['email'])
        if request.method == "POST":
            form = ContactUsForm(request.POST)
            if form.is_valid():
                obj = Query()
                obj.name = form.cleaned_data['name']
                obj.email = User.objects.get(email=form.cleaned_data['email'])
                obj.subject = form.cleaned_data['subject']
                obj.message = form.cleaned_data['message']
                obj.save()
                messages.success(request, "Query Sent Successfully.")
                return redirect('/user')
            else:
                messages.error(request, "Failed to send query.")
                return redirect('/user/contact/')
        else:
            form = ContactUsForm()
            form.initial['name'] = obj.name
            form.initial['email'] = obj.email
            return render(request, "userContact.html", {'name': obj.name, 'form': form, 'count': Cart.objects.filter(user=obj).count()})
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def about(request):
    if 'email' in request.session and User.objects.filter(email=request.session['email']).exists():
        obj = User.objects.get(email=request.session['email'])
        return render(request, 'userAbout.html', {'name': obj.name, 'count': Cart.objects.filter(user=obj).count()})
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def viewProfile(request):
    if 'email' in request.session and User.objects.filter(email=request.session['email']).exists():
        obj = User.objects.get(email=request.session['email'])
        return render(request, 'userProfile.html', {'name': obj.name, 'obj': obj, 'count': Cart.objects.filter(user=obj).count()})
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def resetPassword(request):
    if 'email' in request.session and User.objects.filter(email=request.session['email']).exists():
        obj = User.objects.get(email=request.session['email'])
        if request.method == "POST":
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                old_password = form.cleaned_data['old_password']
                new_password = form.cleaned_data['re_password']
                if old_password != obj.password:
                    messages.error(request, "Wrong old password.\\nTry again!")
                    return redirect('/user/resetPassword/')
                elif new_password == obj.password:
                    messages.error(request, "New password is same as old password.\\nTry again!")
                    return redirect('/user/resetPassword/')
                else:
                    obj.password = new_password
                    obj.save()
                    messages.success(request, "Password reset successfully.")
                    return redirect('/user/profile/')
            else:
                messages.error(request, "Failed to reset password.\\nTry again!")
                return redirect('/user/resetPassword/')
        else:
            form = ResetPasswordForm()
            return render(request, 'userResetPassword.html', {'name': obj.name, 'form': form, 'count': Cart.objects.filter(user=obj).count()})
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def updateProfile(request):
    if 'email' in request.session and User.objects.filter(email=request.session['email']).exists():
        obj = User.objects.get(email=request.session['email'])
        if request.method == "POST":
            form = UpdateProfileForm(request.POST)
            if form.is_valid():
                obj.name = form.cleaned_data['name']
                obj.contact = form.cleaned_data['contact']
                obj.save()
                messages.success(request, "Profile updated successfully.")
                return redirect('/user/profile/')
            else:
                messages.error(request, "Failed to update profile.\\nTry again!")
                return redirect('/user/updatePassword/')
        else:
            form = UpdateProfileForm()
            form.initial['name'] = obj.name
            form.initial['contact'] = obj.contact
            return render(request, 'userUpdateProfile.html', {'name': obj.name, 'obj': obj, 'form': form, 'count': Cart.objects.filter(user=obj).count()})
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def logout(request):
    obj = Cart.objects.filter(user=User.objects.get(email=request.session['email']))
    if obj.exists():
        for i in obj:
            i.delete()
    request.session.flush()
    request.session.clear_expired()
    messages.success(request, "Logged Out Successfully.")
    return redirect('/')

def browseRestaurant(request):
    if 'email' in request.session and User.objects.filter(email=request.session['email']).exists():
        obj = User.objects.get(email=request.session['email'])
        obj1 = Restaurant.objects.filter(status=True)
        obj2 = []
        for i in obj1:
            if datetime.now().strftime('%A') in i.working_days and int(datetime.now().strftime('%H')) >= i.opening_time and int(datetime.now().strftime('%H')) < i.closing_time:
                obj2.append(i)
        cuisines, cost_for_twos = {}, {}
        for i in obj2:
            cuisines[i.restaurant_id] = i.cuisine.strip("[]").replace("'", "")
            cost_for_twos[i.restaurant_id] = "Rs " + str(i.cost_for_two).split(".")[0] + " for two"
        return render(request, 'userBrowse.html', {'name': obj.name, 'obj': obj2, 'cuisines': cuisines, 'cost_for_twos': cost_for_twos, 'count': Cart.objects.filter(user=obj).count()})
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def restaurantMenu(request, id):
    if 'email' in request.session and User.objects.filter(email=request.session['email']).exists():
        obj = User.objects.get(email=request.session['email'])
        res = Restaurant.objects.get(restaurant_id=id)
        cuisines, cost_for_twos = res.cuisine.strip("[]").replace("'", ""), "Rs " + str(res.cost_for_two).split(".")[0] + " for two"
        obj1 = Category.objects.filter(restaurant=res)
        if not obj1.exists():
            obj1 = None
            return render(request, "userRestaurantMenu.html", {'name': obj.name, 'category_object': obj1, 'res': res, 'count': Cart.objects.filter(user=obj).count()})
        else:
            values = {}
            carts = {}
            for i in obj1:
                temp = Item.objects.filter(category=i)
                for j in temp:
                    if i.category in values:
                        values[i.category].append(j)
                    else:
                        values[i.category] = [j]
                    carts[j.name] = []
                    if Cart.objects.filter(user=obj, restaurant=res, category=i, item=j).exists():
                        carts[j.name] = Cart.objects.get(user=obj, restaurant=res, category=i, item=j)
                    else:
                        carts[j.name] = False
            return render(request, "userRestaurantMenu.html", {'name': obj.name, 'category_object': obj1, 'res': res, 'item_object': values, 'cart_object': carts, 'cuisines': cuisines, 'cost_for_twos': cost_for_twos, 'range': range(1, 21), 'count': Cart.objects.filter(user=obj).count()})
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def addToCart(request):
    if 'email' in request.session and User.objects.filter(email=request.session['email']).exists():
        if request.method == "POST":
            obj = User.objects.get(email=request.session['email'])
            res = request.POST['restaurant']
            cat = request.POST['category']
            item = request.POST['item']
            res_obj = Restaurant.objects.get(restaurant_id=res)
            cat_obj = Category.objects.get(restaurant=res_obj, category=cat)
            item_obj = Item.objects.get(category=cat_obj, name=item)
            amount = request.POST.get('amount', False)
            if amount:
                if Cart.objects.filter(user=obj).exists():
                    if Cart.objects.filter(user=obj, restaurant=res_obj).exists():
                        if Cart.objects.filter(user=obj, restaurant=res_obj, category=cat_obj, item=item_obj).exists():
                            cart_obj = Cart.objects.get(user=obj, restaurant=res_obj, category=cat_obj, item=item_obj)
                            cart_obj.quantity = int(amount)
                            cart_obj.save()
                            messages.success(request, "Item updated to cart successfully.")
                            return redirect('/user/browseRestaurant/' + res)
                        else:
                            cart_obj = Cart()
                            cart_obj.user = obj
                            cart_obj.restaurant = res_obj
                            cart_obj.category = cat_obj
                            cart_obj.item = item_obj
                            cart_obj.quantity = int(amount)
                            cart_obj.save()
                            messages.success(request, "Item added to cart successfully.")
                            return redirect('/user/browseRestaurant/' + res)
                    else:
                        messages.error(request, "You can order items from only one restaurant.\\n\\nItems from another restaurant already exists in your cart.\\n\\nPlease remove all items of the other restaurant from your cart to add items from this restaurant.")
                        return redirect('/user/browseRestaurant/' + res)
                else:
                    cart_obj = Cart()
                    cart_obj.user = obj
                    cart_obj.restaurant = res_obj
                    cart_obj.category = cat_obj
                    cart_obj.item = item_obj
                    cart_obj.quantity = int(amount)
                    cart_obj.save()
                    messages.success(request, "Item added to cart successfully.")
                    return redirect('/user/browseRestaurant/' + res)
            else:
                messages.error(request, "Please select/update quantity.")
                return redirect('/user/browseRestaurant/'+res)
        else:
            return redirect('/user/browseRestaurant/')
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def removeFromCart(request, restaurant, category, item):
    if 'email' in request.session and User.objects.filter(email=request.session['email']).exists():
        obj = User.objects.get(email=request.session['email'])
        if Restaurant.objects.filter(restaurant_id=restaurant).exists():
            res_obj = Restaurant.objects.get(restaurant_id=restaurant)
            if Category.objects.filter(restaurant=res_obj, category=category).exists():
                cat_obj = Category.objects.get(restaurant=res_obj, category=category)
                if Item.objects.filter(category=cat_obj, name=item).exists():
                    item_obj = Item.objects.get(category=cat_obj, name=item)
                    if Cart.objects.filter(user=obj, restaurant=res_obj, category=cat_obj, item=item_obj).exists():
                        cart_obj = Cart.objects.get(user=obj, restaurant=res_obj, category=cat_obj, item=item_obj)
                        cart_obj.delete()
                        messages.success(request, "Item removed from cart successfully.")
                        return redirect('/user/browseRestaurant/' + restaurant)
                    else:
                        return redirect('/user/browseRestaurant/')
                else:
                    return redirect('/user/browseRestaurant/')
            else:
                return redirect('/user/browseRestaurant/')
        else:
            return redirect('/user/browseRestaurant/')
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def viewCart(request):
    if 'email' in request.session and User.objects.filter(email=request.session['email']).exists():
        obj = User.objects.get(email=request.session['email'])
        obj1 = Cart.objects.filter(user=obj)
        if obj1.exists():
            res = obj1[0].restaurant.restaurant_name
            quantity, price = {}, {}
            total = 0
            for i in obj1:
                quantity[i.item.name] = str(i.quantity) + " x " + i.item.quantity
                price[i.item.name] = "Rs " + str(int(i.quantity * i.item.price))
                total += i.quantity * i.item.price
            total = int(total)
            gt = total + 25
            return render(request, 'userCart.html', {'name': obj.name, 'obj': obj1, 'res': res, 'quantity': quantity, 'price': price, 'range': range(1, 21), 'total': "Rs " + str(total), 'gt': "Rs " + str(gt), 'count': Cart.objects.filter(user=obj).count()})
        else:
            return render(request, 'userCart.html', {'name': obj.name, 'obj': obj1, 'count': Cart.objects.filter(user=obj).count()})
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def updateCart(request):
    if 'email' in request.session and User.objects.filter(email=request.session['email']).exists():
        obj = User.objects.get(email=request.session['email'])
        if request.method == "POST":
            res = request.POST['restaurant']
            cat = request.POST['category']
            item = request.POST['item']
            res_obj = Restaurant.objects.get(restaurant_id=res)
            cat_obj = Category.objects.get(restaurant=res_obj, category=cat)
            item_obj = Item.objects.get(category=cat_obj, name=item)
            amount = request.POST.get('amount', False)
            if amount:
                cart_obj = Cart.objects.get(user=obj, restaurant=res_obj, category=cat_obj, item=item_obj)
                cart_obj.quantity = amount
                cart_obj.save()
                messages.success(request, "Item updated to cart successfully.")
                return redirect('/user/cart/')
            else:
                messages.error(request, "Please select/update quantity.")
                return redirect('/user/cart/')
        else:
            return redirect('/user/cart/')
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def deleteFromCart(request, restaurant, category, item):
    if 'email' in request.session and User.objects.filter(email=request.session['email']).exists():
        obj = User.objects.get(email=request.session['email'])
        if Restaurant.objects.filter(restaurant_id=restaurant).exists():
            res_obj = Restaurant.objects.get(restaurant_id=restaurant)
            if Category.objects.filter(restaurant=res_obj, category=category).exists():
                cat_obj = Category.objects.get(restaurant=res_obj, category=category)
                if Item.objects.filter(category=cat_obj, name=item).exists():
                    item_obj = Item.objects.get(category=cat_obj, name=item)
                    if Cart.objects.filter(user=obj, restaurant=res_obj, category=cat_obj, item=item_obj).exists():
                        cart_obj = Cart.objects.get(user=obj, restaurant=res_obj, category=cat_obj, item=item_obj)
                        cart_obj.delete()
                        messages.success(request, "Item removed from cart successfully.")
        return redirect('/user/cart/')
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def proceed(request):
    if 'email' in request.session and User.objects.filter(email=request.session['email']).exists():
        obj = User.objects.get(email=request.session['email'])
        if request.method == "POST":
            obj1 = Address.objects.filter(user=obj)
            if not obj1.exists():
                obj1 = None
            form = AddressForm()
            return render(request, 'userProceed.html', {'name': obj.name, 'obj': obj1, 'count': Cart.objects.filter(user=obj).count(), 'form': form})
        else:
            return redirect('/user/cart/')
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def final(request):
    if 'email' in request.session and User.objects.filter(email=request.session['email']).exists():
        obj = User.objects.get(email=request.session['email'])
        if request.method == "POST":
            obj1 = Cart.objects.filter(user=obj)
            res = obj1[0].restaurant.restaurant_name
            quantity, price = {}, {}
            total = 0
            for i in obj1:
                quantity[i.item.name] = str(i.quantity) + " x " + i.item.quantity
                price[i.item.name] = "Rs " + str(int(i.quantity * i.item.price))
                total += i.quantity * i.item.price
            total = int(total)
            gt = total + 25
            idValue = request.POST['address']
            address = Address.objects.get(address_id=idValue, user=obj)
            return render(request, 'userFinal.html', {'name': obj.name, 'obj': obj1, 'res': res, 'quantity': quantity, 'price': price, 'range': range(1, 21), 'total': "Rs " + str(total), 'gt': "Rs " + str(gt), 'count': Cart.objects.filter(user=obj).count(), 'address': address})
        else:
            return redirect('/user/cart/')
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def generateId(request):
    id_list = list(Address.objects.values_list('address_id', flat=True))
    while True:
        id = ''.join(random.choice(string.ascii_letters) for x in range(5)) + str(random.randint(10000, 99999))
        if id not in id_list:
            return id

def saveAndFinal(request):
    if 'email' in request.session and User.objects.filter(email=request.session['email']).exists():
        obj = User.objects.get(email=request.session['email'])
        if request.method == "POST":
            form = AddressForm(request.POST)
            if form.is_valid():
                address_obj = Address()
                address_obj.address_id = generateId(request)
                address_obj.user = obj
                address_obj.line1 = form.cleaned_data['line1']
                address_obj.line2 = form.cleaned_data['line2']
                address_obj.landmark = form.cleaned_data['landmark']
                address_obj.locality = form.cleaned_data['locality']
                address_obj.city = form.cleaned_data['city']
                address_obj.zip = form.cleaned_data['zip']
                address_obj.save()
                obj1 = Cart.objects.filter(user=obj)
                res = obj1[0].restaurant.restaurant_name
                quantity, price = {}, {}
                total = 0
                for i in obj1:
                    quantity[i.item.name] = str(i.quantity) + " x " + i.item.quantity
                    price[i.item.name] = "Rs " + str(int(i.quantity * i.item.price))
                    total += i.quantity * i.item.price
                total = int(total)
                gt = total + 25
                return render(request, 'userFinal.html', {'name': obj.name, 'obj': obj1, 'res': res, 'quantity': quantity, 'price': price, 'range': range(1, 21), 'total': "Rs " + str(total), 'gt': "Rs " + str(gt), 'count': Cart.objects.filter(user=obj).count(), 'address': address_obj})
            else:
                messages.error(request, "Unable to add new address.")
                return redirect('/user/cart/')
        else:
            return redirect('/user/cart/')
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def order(request):
    if 'email' in request.session and User.objects.filter(email=request.session['email']).exists():
        obj = User.objects.get(email=request.session['email'])
        if request.method == "POST":
            cart_obj = Cart.objects.filter(user=obj)
            res = cart_obj[0].restaurant
            if datetime.now().strftime('%A') in res.working_days and int(datetime.now().strftime('%H')) >= res.opening_time and int(datetime.now().strftime('%H')) < res.closing_time:
                address = Address.objects.get(address_id=request.POST['address'])
                order_obj = Orders()
                order_obj.order_number = random.randint(100000000000, 999999999999)
                order_obj.restaurant = cart_obj[0].restaurant
                order_obj.user = obj
                order_obj.address = address
                items, quantity = [], []
                total = 0
                for i in cart_obj:
                    items.append(i.item.name)
                    quantity.append(str(i.quantity) + " x " + i.item.quantity)
                    total += i.quantity * i.item.price
                order_obj.items = items
                order_obj.quantity = quantity
                order_obj.total = int(total) + 25
                order_obj.save()
                for i in cart_obj:
                    i.delete()
                obj1 = Orders.objects.filter(user=obj, delivered=False)
                items = {}
                for i in obj1:
                    items[i.order_number] = [j.strip("'") for j in i.items.strip('[]').split(', ')]
                quantity = {}
                for i in obj1:
                    quantity[i.order_number] = [j.strip("'") for j in i.quantity.strip('[]').split(', ')]
                name, contact = {}, {}
                for i in obj1:
                    if i.delivery:
                        obj2 = Delivery.objects.get(delivery_id=i.delivery)
                        if i.order_number not in name.keys():
                            name[i.order_number] = [obj2.name]
                            contact[i.order_number] = [obj2.contact]
                        else:
                            name[i.order_number].append(obj2.name)
                            contact[i.order_number].append(obj2.contact)
                messages.success(request, "Order Placed Successfully\\n\\nPlease pay Rs " + str(int(total) + 25) + " in Cash to the Delivery Person.")
                return render(request, 'userOrder.html', {'name': obj.name, 'obj': obj1, 'items': items, 'quantity': quantity, 'delivery_name': name, 'delivery_contact': contact, 'count': Cart.objects.filter(user=obj).count()})
            else:
                for i in cart_obj:
                    i.delete()
                messages.error(request, "Sorry! The restaurant is currently unavailable for accepting orders.\\n\\nPlease order items from any other restaurant")
                return redirect('/user/browseRestaurant/')
        else:
            obj1 = Orders.objects.filter(user=obj, delivered=False)
            if obj1.exists():
                items = {}
                for i in obj1:
                    items[i.order_number] = [j.strip("'") for j in i.items.strip('[]').split(', ')]
                quantity = {}
                for i in obj1:
                    quantity[i.order_number] = [j.strip("'") for j in i.quantity.strip('[]').split(', ')]
                name, contact = {}, {}
                for i in obj1:
                    if i.delivery:
                        obj2 = Delivery.objects.get(delivery_id=i.delivery)
                        if i.order_number not in name.keys():
                            name[i.order_number] = [obj2.name]
                            contact[i.order_number] = [obj2.contact]
                        else:
                            name[i.order_number].append(obj2.name)
                            contact[i.order_number].append(obj2.contact)
                return render(request, 'userOrder.html', {'name': obj.name, 'obj': obj1, 'items': items, 'quantity': quantity, 'delivery_name': name, 'delivery_contact': contact, 'count': Cart.objects.filter(user=obj).count()})
            else:
                obj1 = None
                return render(request, 'userOrder.html', {'name': obj.name, 'obj': obj1, 'count': Cart.objects.filter(user=obj).count()})
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def orderHistory(request):
    if 'email' in request.session and User.objects.filter(email=request.session['email']).exists():
        obj = User.objects.get(email=request.session['email'])
        obj1 = Orders.objects.filter(user=obj, delivered=True)
        if obj1.exists():
            items = {}
            for i in obj1:
                items[i.order_number] = [j.strip("'") for j in i.items.strip('[]').split(', ')]
            quantity = {}
            for i in obj1:
                quantity[i.order_number] = [j.strip("'") for j in i.quantity.strip('[]').split(', ')]
            name, contact = {}, {}
            for i in obj1:
                if i.delivery:
                    obj2 = Delivery.objects.get(delivery_id=i.delivery)
                    if i.order_number not in name.keys():
                        name[i.order_number] = [obj2.name]
                        contact[i.order_number] = [obj2.contact]
                    else:
                        name[i.order_number].append(obj2.name)
                        contact[i.order_number].append(obj2.contact)
            return render(request, 'userOrderHistory.html', {'name': obj.name, 'obj': obj1, 'items': items, 'quantity': quantity, 'delivery_name': name, 'delivery_contact': contact, 'count': Cart.objects.filter(user=obj).count()})
        else:
            obj1 = None
            return render(request, 'userOrderHistory.html', {'name': obj.name, 'obj': obj1, 'count': Cart.objects.filter(user=obj).count()})
    else:
        messages.error(request, "Please login first.")
        return redirect('/')