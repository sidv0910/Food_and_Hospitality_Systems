import os, random
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from wsgiref.util import FileWrapper
import mimetypes
from django.http import HttpResponse
from .forms import ContactUsForm, CategoryForm, CategoryItemForm, ResetPasswordForm, UpdateProfileForm
from .models import Query, Category, Item, Orders
from Home.models import Restaurant, Delivery

def homepage(request):
    if 'email' in request.session and Restaurant.objects.filter(restaurant_email=request.session['email']).exists():
        obj = Restaurant.objects.get(restaurant_email=request.session['email'])
        return render(request, 'restaurantIndex.html', {'name': obj.restaurant_name})
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def contact(request):
    if 'email' in request.session and Restaurant.objects.filter(restaurant_email=request.session['email']).exists():
        if request.method == "POST":
            form = ContactUsForm(request.POST)
            if form.is_valid():
                obj = Query()
                obj.name = form.cleaned_data['name']
                obj.email = Restaurant.objects.get(restaurant_email=form.cleaned_data['email'])
                obj.subject = form.cleaned_data['subject']
                obj.message = form.cleaned_data['message']
                obj.save()
                messages.success(request, "Query Sent Successfully.")
                return redirect('/restaurant')
            else:
                messages.error(request, "Failed to send query.")
                return redirect('/restaurant/contact')
        else:
            obj = Restaurant.objects.get(restaurant_email=request.session['email'])
            form = ContactUsForm()
            form.initial['name'] = obj.restaurant_name
            form.initial['email'] = obj.restaurant_email
            return render(request, "restaurantContact.html", {'name': obj.restaurant_name, 'form': form})
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def about(request):
    if 'email' in request.session and Restaurant.objects.filter(restaurant_email=request.session['email']).exists():
        obj = Restaurant.objects.get(restaurant_email=request.session['email'])
        return render(request, 'restaurantAbout.html', {'name': obj.restaurant_name})
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def viewProfile(request):
    if 'email' in request.session and Restaurant.objects.filter(restaurant_email=request.session['email']).exists():
        obj = Restaurant.objects.get(restaurant_email=request.session['email'])
        cuisines = ['North Indian', 'South Indian', 'Fast Food', 'Beverages', 'Bakery', 'Desserts', 'Italian']
        cuisine = obj.cuisine.strip('['']').split(', ')
        for i in range(len(cuisine)):
            cuisine[i] = cuisine[i].strip("'")
        cuisine_data = {}
        for i in cuisines:
            check = False
            for j in cuisine:
                if i == j:
                    check = True
            cuisine_data[i] = check
        workingDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        workingDay = obj.working_days.strip('['']').split(', ')
        for i in range(len(workingDay)):
            workingDay[i] = workingDay[i].strip("'")
        workingDay_data = {}
        for i in workingDays:
            check = False
            for j in workingDay:
                if i == j:
                    check = True
            workingDay_data[i] = check
        if obj.opening_time < 12:
            start = str(obj.opening_time) + " a.m."
        elif obj.opening_time == 12:
            start = str(obj.opening_time) + " noon"
        else:
            start = str(obj.opening_time - 12) + " p.m."
        if obj.closing_time < 12:
            end = str(obj.closing_time) + " a.m."
        elif obj.closing_time == 12:
            end = str(obj.closing_time) + " noon"
        else:
            end = str(obj.closing_time - 12) + " p.m."
        return render(request, 'viewProfile.html', {'name': obj.restaurant_name, 'obj': obj, 'start': start, 'end': end, 'cuisine': cuisine_data, 'working_day': workingDay_data})
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def resetPassword(request):
    if 'email' in request.session and Restaurant.objects.filter(restaurant_email=request.session['email']).exists():
        obj = Restaurant.objects.get(restaurant_email=request.session['email'])
        if request.method == "POST":
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                old_password = form.cleaned_data['old_password']
                new_password = form.cleaned_data['re_password']
                if old_password != obj.password:
                    messages.error(request, "Wrong old password.\\nTry again!")
                    return redirect('/restaurant/resetPassword')
                elif new_password == obj.password:
                    messages.error(request, "New password is same as old password.\\nTry again!")
                    return redirect('/restaurant/resetPassword')
                else:
                    obj.password = new_password
                    obj.save()
                    messages.success(request, "Password reset successfully.")
                    return redirect('/restaurant/viewProfile')
            else:
                messages.error(request, "Failed to reset password.\\nTry again!")
                return redirect('/restaurant/resetPassword')
        else:
            form = ResetPasswordForm()
            return render(request, 'resetPassword.html', {'name': obj.restaurant_name, 'form': form})
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def updateProfile(request):
    if 'email' in request.session and Restaurant.objects.filter(restaurant_email=request.session['email']).exists():
        obj = Restaurant.objects.get(restaurant_email=request.session['email'])
        if request.method == "POST":
            form = UpdateProfileForm(request.POST)
            if form.is_valid():
                obj.owner_name = form.cleaned_data['owner_name']
                obj.address = form.cleaned_data['address']
                obj.city = form.cleaned_data['city']
                obj.zip = form.cleaned_data['zip']
                obj.restaurant_contact = form.cleaned_data['restaurant_contact']
                obj.cost_for_two = form.cleaned_data['cost_for_two']
                obj.outlets = form.cleaned_data['outlets']
                obj.cuisine = str(request.POST['cuisines'].split(','))
                obj.working_days = str(request.POST['working_day'].split(','))
                obj.opening_time = request.POST.get('from_time', obj.opening_time)
                obj.closing_time = request.POST.get('to_time', obj.closing_time)
                obj.save()
                messages.success(request, "Profile updated successfully.")
                return redirect('/restaurant/viewProfile')
            else:
                messages.error(request, "Failed to update profile.\\nTry again!")
                return redirect('/restaurant/updatePassword')
        else:
            form = UpdateProfileForm()
            form.initial['owner_name'] = obj.owner_name
            form.initial['address'] = obj.address
            form.initial['city'] = obj.city
            form.initial['zip'] = obj.zip
            form.initial['restaurant_contact'] = obj.restaurant_contact
            form.initial['cost_for_two'] = obj.cost_for_two
            form.initial['outlets'] = obj.outlets
            times = {8: '8 a.m.', 9: '9 a.m.', 10: '10 a.m.', 11: '11 a.m.', 12: '12 noon', 13: '1 p.m.', 14: '2 p.m.', 15: '3 p.m.', 16: '4 p.m.', 17: '5 p.m.', 18: '6 p.m.', 19: '7 p.m.', 20: '8 p.m.', 21: '9 p.m.', 22: '10 p.m.'}
            cuisines = ['North Indian', 'South Indian', 'Fast Food', 'Beverages', 'Bakery', 'Desserts', 'Italian']
            cuisine = obj.cuisine.strip('['']').split(', ')
            for i in range(len(cuisine)):
                cuisine[i] = cuisine[i].strip("'")
            cuisine_data = {}
            for i in cuisines:
                check = False
                for j in cuisine:
                    if i == j:
                        check = True
                cuisine_data[i] = check
            workingDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            workingDay = obj.working_days.strip('['']').split(', ')
            for i in range(len(workingDay)):
                workingDay[i] = workingDay[i].strip("'")
            workingDay_data = {}
            for i in workingDays:
                check = False
                for j in workingDay:
                    if i == j:
                        check = True
                workingDay_data[i] = check
            return render(request, 'updateProfile.html', {'name': obj.restaurant_name, 'obj': obj, 'form': form, 'times': times, 'cuisine': cuisine_data, 'working_day': workingDay_data})
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def logout(request):
    request.session.flush()
    request.session.clear_expired()
    messages.success(request, "Logged Out Successfully.")
    return redirect('/')

def menu(request):
    if 'email' in request.session and Restaurant.objects.filter(restaurant_email=request.session['email']).exists():
        obj = Restaurant.objects.get(restaurant_email=request.session['email'])
        obj1 = Category.objects.filter(restaurant=obj)
        pair = []
        for i in obj1:
            temp = Item.objects.filter(category=i)
            for j in temp:
                pair.append(j)
        if not obj1.exists():
            obj1 = None
        return render(request, "restaurantMenu.html", {'name': obj.restaurant_name, 'category_object': obj1, 'item_object': pair})
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def addCategory(request):
    if 'email' in request.session and Restaurant.objects.filter(restaurant_email=request.session['email']).exists():
        obj = Restaurant.objects.get(restaurant_email=request.session['email'])
        form = CategoryForm()
        return render(request, 'addCategory.html', {'name': obj.restaurant_name, 'form': form})
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def addCategoryItem(request):
    if 'email' in request.session and Restaurant.objects.filter(restaurant_email=request.session['email']).exists():
        obj = Restaurant.objects.get(restaurant_email=request.session['email'])
        if request.method == "POST":
            categoryItemForm = CategoryItemForm(request.POST)
            if categoryItemForm.is_valid():
                if Item.objects.filter(name=categoryItemForm.cleaned_data['item']).exists():
                    messages.error(request, "Item already exists.\\nTry again!")
                    return redirect('/restaurant/menu/')
                else:
                    obj1 = Category()
                    obj1.restaurant = obj
                    obj1.category = categoryItemForm.cleaned_data['category']
                    obj1.save()
                    obj2 = Item()
                    obj2.category = obj1
                    obj2.name = categoryItemForm.cleaned_data['item']
                    obj2.quantity = request.POST['quantity']
                    obj2.item_type = request.POST['item_type']
                    obj2.price = categoryItemForm.cleaned_data['price']
                    obj2.save()
                    messages.success(request, "Category and Item added successfully.")
                    return redirect('/restaurant/menu')
        else:
            categoryForm = CategoryForm(request.GET)
            if categoryForm.is_valid():
                category = categoryForm.cleaned_data['category']
                category = category.title()
                if Category.objects.filter(restaurant=obj, category=category).exists():
                    messages.error(request, "Category already exists.\\nTry again!")
                    return redirect('/restaurant/addCategory/')
                else:
                    item = False
                    form = CategoryItemForm()
                    form.initial['category'] = category
                    return render(request, 'addCategoryItem.html', {'name': obj.restaurant_name, 'form': form, 'item': item})
            else:
                messages.error(request, "Failed to add category of items.\\nTry again!")
                return redirect('/restaurant/addCategory/')
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def addItem(request, category):
    if 'email' in request.session and Restaurant.objects.filter(restaurant_email=request.session['email']).exists():
        obj = Restaurant.objects.get(restaurant_email=request.session['email'])
        if request.method == "POST":
            form = CategoryItemForm(request.POST)
            if form.is_valid():
                if Item.objects.filter(category=Category.objects.get(restaurant=obj, category=category), name=form.cleaned_data['item']).exists():
                    messages.error(request, "Item already exists.\\nTry again!")
                    return redirect('/restaurant/menu/')
                else:
                    obj1 = Category.objects.get(restaurant=obj, category=category)
                    obj2 = Item()
                    obj2.category = obj1
                    obj2.name = form.cleaned_data['item']
                    obj2.quantity = request.POST.get('quantity', False)
                    obj2.item_type = request.POST.get('item_type', False)
                    obj2.price = form.cleaned_data['price']
                    obj2.save()
                    messages.success(request, "Item added successfully.")
                    return redirect('/restaurant/menu')
            else:
                messages.error(request, "Unable to add item to the menu.")
                return redirect('/restaurant/menu')
        else:
            item = category
            form = CategoryItemForm()
            form.initial['category'] = category
            return render(request, 'addCategoryItem.html', {'name': obj.restaurant_name, 'form': form, 'item': item})
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def deleteCategory(request, category):
    if 'email' in request.session and Restaurant.objects.filter(restaurant_email=request.session['email']).exists():
        obj = Restaurant.objects.get(restaurant_email=request.session['email'])
        obj1 = Category.objects.get(restaurant=obj, category=category)
        obj1.delete()
        messages.success(request, "Category Deleted Successfully")
        return redirect('/restaurant/menu')
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def deleteItem(request, category, item):
    if 'email' in request.session and Restaurant.objects.filter(restaurant_email=request.session['email']).exists():
        obj = Restaurant.objects.get(restaurant_email=request.session['email'])
        obj1 = Category.objects.get(restaurant=obj, category=category)
        obj2 = Item.objects.get(category=obj1, name=item)
        obj2.delete()
        if not Item.objects.filter(category=obj1).exists():
            obj1.delete()
        messages.success(request, "Item Deleted Successfully")
        return redirect('/restaurant/menu')
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def updateCategory(request, category):
    if 'email' in request.session and Restaurant.objects.filter(restaurant_email=request.session['email']).exists():
        obj = Restaurant.objects.get(restaurant_email=request.session['email'])
        if request.method == "POST":
            form = CategoryForm(request.POST)
            if form.is_valid():
                if Category.objects.filter(restaurant=obj, category=form.cleaned_data['category']).exists():
                    messages.error(request, "New Category Name already exists.\\nTry Again!")
                    return redirect('/restaurant/updateCategory/'+category)
                else:
                    obj1 = Category.objects.get(restaurant=obj, category=category)
                    obj1.category = form.cleaned_data['category']
                    obj1.save()
                    messages.success(request, "Category Name updated successfully.")
                    return redirect('/restaurant/menu/')
            else:
                messages.error(request, "Unable to update the category.")
                return redirect('/restaurant/menu')
        else:
            form = CategoryForm()
            return render(request, 'updateCategory.html', {'name': obj.restaurant_name, 'form': form, 'item': category})
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def updateItem(request, category, item):
    if 'email' in request.session and Restaurant.objects.filter(restaurant_email=request.session['email']).exists():
        obj = Restaurant.objects.get(restaurant_email=request.session['email'])
        if request.method == "POST":
            obj1 = Category.objects.get(restaurant=obj, category=category)
            obj2 = Item.objects.get(category=obj1, name=item)
            category_name = request.POST.get('category', category)
            obj2.category = Category.objects.get(restaurant=obj, category=category_name)
            obj2.quantity = request.POST.get('quantity', obj2.quantity)
            obj2.item_type = request.POST.get('item_type', obj2.item_type)
            obj2.price = request.POST.get('price', obj2.price)
            obj2.save()
            if not Item.objects.filter(category=obj1).exists():
                obj1.delete()
            messages.success(request, "Item updated successfully.")
            return redirect('/restaurant/menu/')
        else:
            category_data = Category.objects.get(restaurant=obj, category=category)
            item_data = Item.objects.get(category=category_data, name=item)
            category_list = list(Category.objects.filter(restaurant=obj).values_list('category', flat=True))
            quantity_data_1 = ["Quarter Plate", "Half Plate", "Full Plate"]
            quantity_data_2 = ["100 ml", "250 ml", "500 ml", "1 L"]
            quantity_data_3 = ["100 gm", "250 gm", "500 gm", "1 kg"]
            item_type_data = ["Veg", "Non-Veg", "Egg"]
            return render(request, 'updateItem.html', {'name': obj.restaurant_name, 'category_obj': category_data, 'item_obj': item_data, 'category_list': category_list, 'quantity_obj_1': quantity_data_1, 'quantity_obj_2': quantity_data_2, 'quantity_obj_3': quantity_data_3, 'item_type_obj': item_type_data})
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def download_image(request, image):
    if 'email' in request.session and Restaurant.objects.filter(restaurant_email=request.session['email']).exists():
        obj = Restaurant.objects.get(restaurant_email=request.session['email'])
        if image == "facade":
            img = obj.facade
        elif image == "kitchen":
            img = obj.kitchen
        elif image == "dining_packaging":
            img = obj.dining_packaging
        elif image == "locality":
            img = obj.locality
        elif image == "shop_license":
            img = obj.shop_license
        elif image == "fssai":
            img = obj.fssai
        elif image == "gstin_pan":
            img = obj.gstin_pan
        elif image == "menu":
            img = obj.menu
        else:
            return redirect('/restaurant/viewProfile')
        wrapper = FileWrapper(open(str(img.file), 'rb'))
        content_type = mimetypes.guess_type(img.name.split('/')[-1])[0]
        response = HttpResponse(wrapper, content_type=content_type)
        response['Content-Length'] = os.path.getsize(str(img.file))
        response['Content-Disposition'] = "attachment; filename=%s" % img.name.split('/')[-1]
        return response
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def order(request):
    if 'email' in request.session and Restaurant.objects.filter(restaurant_email=request.session['email']).exists():
        obj = Restaurant.objects.get(restaurant_email=request.session['email'])
        obj1 = Orders.objects.filter(restaurant=obj, delivered=False)
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
            return render(request, 'orders.html', {'name': obj.restaurant_name, 'obj': obj1, 'items': items, 'quantity': quantity, 'delivery_name': name, 'delivery_contact': contact})
        else:
            obj1 = None
            return render(request, 'orders.html', {'name': obj.restaurant_name, 'obj': obj1})
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def updateOrder(request):
    if 'email' in request.session and Restaurant.objects.filter(restaurant_email=request.session['email']).exists():
        obj = Restaurant.objects.get(restaurant_email=request.session['email'])
        if request.method == "POST":
            order_id = request.POST['order_id']
            obj1 = Orders.objects.get(order_number=order_id)
            if obj1.accepted:
                if obj1.food_is_being_prepared:
                    if obj1.ready_for_delivery:
                        return redirect('/restaurant/order/')
                    else:
                        obj1.ready_for_delivery = True
                else:
                    obj1.food_is_being_prepared = True
            else:
                obj1.accepted = True
            if not obj1.delivery:
                choices = Delivery.objects.filter(status=False)
                if choices.exists():
                    choices = list(choices)
                    selected = random.choice(choices)
                    obj1.delivery = selected.delivery_id
                    selected.status = True
                    selected.save()
            obj1.save()
            return redirect('/restaurant/order')
        else:
            return redirect('/restaurant/order')
    else:
        messages.error(request, "Please login first.")
        return redirect('/')

def orderHistory(request):
    if 'email' in request.session and Restaurant.objects.filter(restaurant_email=request.session['email']).exists():
        obj = Restaurant.objects.get(restaurant_email=request.session['email'])
        obj1 = Orders.objects.filter(restaurant=obj, delivered=True)
        if obj1.exists():
            items = {}
            for i in obj1:
                items[i.order_number] = [j.strip("'") for j in i.items.strip('[]').split(', ')]
            quantity = {}
            for i in obj1:
                quantity[i.order_number] = [j.strip("'") for j in i.quantity.strip('[]').split(', ')]
            name, contact = {}, {}
            for i in obj1:
                obj2 = Delivery.objects.get(delivery_id=i.delivery)
                if i.order_number not in name.keys():
                    name[i.order_number] = [obj2.name]
                    contact[i.order_number] = [obj2.contact]
                else:
                    name[i.order_number].append(obj2.name)
                    contact[i.order_number].append(obj2.contact)
            return render(request, 'orderHistory.html', {'name': obj.restaurant_name, 'obj': obj1, 'items': items, 'quantity': quantity, 'delivery_name': name, 'delivery_contact': contact})
        else:
            obj1 = None
        return render(request, 'orderHistory.html', {'name': obj.restaurant_name, 'obj': obj1})
    else:
        messages.error(request, "Please login first.")
        return redirect('/')