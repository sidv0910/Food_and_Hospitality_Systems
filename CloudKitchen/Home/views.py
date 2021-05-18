from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings
from random import randint
from .forms import RegisterForm, LoginForm, ForgotForm, ResetForm, ContactUsForm, PartnerForm, RestaurantLoginForm, DeliveryLoginForm
from .models import User, Query, Restaurant, Delivery
from Restaurant.models import Category, Item

otp = ""

def homepage(request):
    if 'email' in request.session:
        if User.objects.filter(email=request.session['email']).exists():
            return redirect('/user')
        elif Restaurant.objects.filter(restaurant_email=request.session['email']).exists():
            return redirect('/restaurant')
        elif Delivery.objects.filter(email=request.session['email']).exists():
            return redirect('/delivery')
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                obj = User.objects.get(email=form.cleaned_data['email'])
                if obj.password == form.cleaned_data['password']:
                    request.session['email'] = form.cleaned_data['email']
                    messages.success(request, "Login Successful")
                    return redirect('/user')
                else:
                    messages.error(request, "Email Address and Password do not match.\\nTry Again.")
                    return redirect('/login')
            else:
                messages.error(request, "No user account found for the given email address.")
                return redirect('/login')
        else:
            messages.error(request, "Login Failed.")
            return redirect('/login')
    else:
        form = LoginForm()
        return render(request, "login.html", {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            obj = User()
            obj.name = form.cleaned_data['name']
            obj.email = form.cleaned_data['email']
            obj.contact = form.cleaned_data['contact']
            obj.password = form.cleaned_data['re_password']
            obj.save()
            messages.success(request, "Sign Up Successful")
            return redirect('/login')
        else:
            message = str(form.non_field_errors())
            message = message.split("<li>")
            message = message[1].split("</li>")
            print(message[0])
            messages.error(request, message[0])
            return redirect('/register')
    else:
        form = RegisterForm()
        return render(request, "register.html", {'form': form})

def mail(request, email, otp):
    obj = User.objects.get(email=email)
    subject = "Reset Password"
    message = "Dear " + obj.name + ",\n\nWe received a request from you to reset the password for your Cloud Kitchen account that is associated with this email address.\n\nThe verification code is " + otp + ".\n\nPlease use the above OTP to complete your Reset Password request.\n\nIf you did not make this request, you can safely ignore this email.\n\nThank You,\nCloud Kitchen Team"
    to = [email]
    res = send_mail(subject, message, settings.EMAIL_HOST_USER, to)
    if res == 1:
        return True
    else:
        return False

def forgot(request):
    if request.method == 'POST':
        form = ForgotForm(request.POST)
        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                global otp
                otp = str(randint(100000, 999999))
                if mail(request, form.cleaned_data['email'], otp):
                    request.session['user_email'] = form.cleaned_data['email']
                    return render(request, 'verify.html')
                else:
                    messages.error(request, "Forgot Password Failed.")
                    return redirect('/forgot')
            else:
                messages.error(request, "No user account found for the given email address.")
                return redirect('/forgot')
        else:
            messages.error(request, "Forgot Password Failed.")
            return redirect('/forgot')
    else:
        form = ForgotForm()
        return render(request, "forgot.html", {'form': form})

def verify(request):
    if request.method == "POST":
        first = request.POST['first']
        second = request.POST['second']
        third = request.POST['third']
        fourth = request.POST['fourth']
        fifth = request.POST['fifth']
        sixth = request.POST['sixth']
        user_otp = first + second + third + fourth + fifth + sixth
        if user_otp == otp:
            form = ResetForm()
            return render(request, "reset.html", {'form': form})
        else:
            request.session.flush()
            request.session.clear_expired()
            messages.error(request, "Wrong OTP entered.\\nTry Again.")
            return redirect('/forgot')
    else:
        return forgot(request)

def reset(request):
    if request.method == "POST":
        form = ResetForm(request.POST)
        if form.is_valid():
            obj = User.objects.get(email=request.session['user_email'])
            if obj.password == form.cleaned_data['re_password']:
                messages.error(request, "New Password is same as the Old Password.\\nPlease enter a different password.")
                form = ResetForm()
                return render(request, "reset.html", {'form': form})
            else:
                obj.password = form.cleaned_data['re_password']
                obj.save()
                request.session.flush()
                request.session.clear_expired()
                messages.success(request, "Password Reset Successfully.")
                return redirect('/login')
        else:
            request.session.flush()
            request.session.clear_expired()
            messages.error(request, "Reset Password Failed.\\nTry Again.")
            return redirect('/forgot')
    else:
        return forgot(request)

def contact(request):
    if request.method == "POST":
        form = ContactUsForm(request.POST)
        if form.is_valid():
            obj = Query()
            obj.name = form.cleaned_data['name']
            obj.email = form.cleaned_data['email']
            obj.subject = form.cleaned_data['subject']
            obj.message = form.cleaned_data['message']
            obj.save()
            messages.success(request, "Query Sent Successfully.")
            return redirect('/')
        else:
            messages.error(request, "Failed to send query.")
            return redirect('/contact')
    else:
        form = ContactUsForm()
        return render(request, "contact.html", {'form':form})

def about(request):
    return render(request, "about.html")

def idGenerator(request):
    while True:
        id = "CK" + str(randint(1000, 9999))
        if not Restaurant.objects.filter(restaurant_id=id).exists():
            return id
            break

def confirm_mail(request, name, email):
    subject = "Application Received Successfully"
    message = name + ",\n\nThank you for submitting your application to the Cloud Kitchen.\n\nYour application is under process as we are verifying all the documents provided by you. Once all the documents are verified, you'll receive a mail from our team having your Restaurant ID and then you can go live for accepting orders.\n\nThank You,\nCloud Kitchen Team"
    to = [email]
    res = send_mail(subject, message, settings.EMAIL_HOST_USER, to)
    if res == 1:
        return True
    else:
        return False

def partner(request):
    if request.method == "POST":
        form = PartnerForm(request.POST, request.FILES)
        if form.is_valid():
            if Restaurant.objects.filter(restaurant_email = form.cleaned_data["restaurant_email"]).exists():
                messages.error(request, "A restaurant account with the given email address already exists.\\nTry Again.")
                return redirect('/partner')
            elif User.objects.filter(email = form.cleaned_data["restaurant_email"]).exists():
                messages.error(request, "A user account with the given email address already exists.\\nTry Again.")
                return redirect('/partner')
            else:
                obj = Restaurant()
                id = idGenerator(request)
                obj.restaurant_id = id
                obj.restaurant_name = form.cleaned_data["restaurant_name"]
                obj.owner_name = form.cleaned_data["owner_name"]
                obj.address = form.cleaned_data["address"]
                obj.city = form.cleaned_data["city"]
                obj.zip = form.cleaned_data["zip"]
                obj.restaurant_email = form.cleaned_data["restaurant_email"]
                obj.restaurant_contact = form.cleaned_data["restaurant_contact"]
                obj.password = form.cleaned_data["password"]
                obj.cost_for_two = form.cleaned_data["cost_for_two"]
                obj.outlets = form.cleaned_data["outlets"]
                obj.cuisine = str(form.cleaned_data["cuisine"])
                obj.working_days = str(form.cleaned_data["working_days"])
                obj.opening_time = request.POST["from_time"]
                obj.closing_time = request.POST["to_time"]
                obj.shop_license = request.FILES['shop_license']
                obj.fssai = request.FILES['fssai']
                obj.gstin_pan = request.FILES['gstin_pan']
                obj.menu = request.FILES['menu']
                obj.facade = request.FILES['facade']
                obj.kitchen = request.FILES['kitchen']
                obj.dining_packaging = request.FILES['dining_packaging']
                obj.locality = request.FILES['locality']
                if confirm_mail(request, form.cleaned_data["restaurant_name"], form.cleaned_data["restaurant_email"]):
                    obj.save()
                    messages.success(request, "Application Submitted Successfully")
                    return redirect('/')
                else:
                    messages.error(request, "Failed to submit your application")
                    return redirect('/partner')
        else:
            messages.error(request, "Failed to submit your application")
            return redirect('/partner')
    else:
        form = PartnerForm()
        return render(request, "partner.html", {'form':form})

def restaurantLogin(request):
    if request.method == "POST":
        form = RestaurantLoginForm(request.POST)
        if form.is_valid():
            if Restaurant.objects.filter(restaurant_email=form.cleaned_data['email']).exists():
                obj = Restaurant.objects.get(restaurant_email=form.cleaned_data['email'])
                if obj.restaurant_id == form.cleaned_data["restaurant_id"] and obj.password == form.cleaned_data['password']:
                    request.session['email'] = form.cleaned_data['email']
                    messages.success(request, "Login Successful")
                    return redirect('/restaurant')
                else:
                    messages.error(request, "Restaurant ID, Email Address and Password do not match.\\nTry Again.")
                    return redirect('/restaurantLogin')
            else:
                messages.error(request, "No restaurant account found for the given email address.")
                return redirect('/restaurantLogin')
        else:
            messages.error(request, "Login Failed.")
            return redirect('/restaurantLogin')
    else:
        form = RestaurantLoginForm()
        return render(request, "loginRestaurant.html", {'form':form})

def restaurantMail(request, email, otp):
    obj = Restaurant.objects.get(restaurant_email=email)
    subject = "Reset Password"
    message = obj.restaurant_name + ",\n\nWe received a request from you to reset the password for your Cloud Kitchen account that is associated with this email address.\n\nThe verification code is " + otp + ".\n\nPlease use the above OTP to complete your Reset Password request.\n\nIf you did not make this request, you can safely ignore this email.\n\nThank You,\nCloud Kitchen Team"
    to = [email]
    res = send_mail(subject, message, settings.EMAIL_HOST_USER, to)
    if res == 1:
        return True
    else:
        return False

def restaurantForgot(request):
    if request.method == 'POST':
        form = ForgotForm(request.POST)
        if form.is_valid():
            if Restaurant.objects.filter(restaurant_email=form.cleaned_data['email']).exists():
                obj = Restaurant.objects.get(restaurant_email=form.cleaned_data['email'])
                if obj.status == True:
                    global otp
                    otp = str(randint(100000, 999999))
                    if restaurantMail(request, form.cleaned_data['email'], otp):
                        request.session['restaurant_email'] = form.cleaned_data['email']
                        return render(request, 'restaurantVerify.html')
                    else:
                        messages.error(request, "Forgot Password Failed.")
                        return redirect('/restaurantForgot')
                else:
                    messages.error(request, "Your account is under process. \\nPlease wait until we activate your account.")
                    return redirect('/restaurantForgot')
            else:
                messages.error(request, "No restaurant account found for the given email address.")
                return redirect('/restaurantForgot')
        else:
            messages.error(request, "Forgot Password Failed.")
            return redirect('/restaurantForgot')
    else:
        form = ForgotForm()
        return render(request, "restaurantForgot.html", {'form': form})

def restaurantVerify(request):
    if request.method == "POST":
        first = request.POST['first']
        second = request.POST['second']
        third = request.POST['third']
        fourth = request.POST['fourth']
        fifth = request.POST['fifth']
        sixth = request.POST['sixth']
        user_otp = first + second + third + fourth + fifth + sixth
        if user_otp == otp:
            form = ResetForm()
            return render(request, "restaurantReset.html", {'form': form})
        else:
            request.session.flush()
            request.session.clear_expired()
            messages.error(request, "Wrong OTP entered.\\nTry Again.")
            return redirect('/restaurantForgot')
    else:
        return restaurantForgot(request)

def restaurantReset(request):
    if request.method == "POST":
        form = ResetForm(request.POST)
        if form.is_valid():
            obj = Restaurant.objects.get(restaurant_email=request.session['restaurant_email'])
            if obj.password == form.cleaned_data['re_password']:
                messages.error(request, "New Password is same as the Old Password.\\nPlease enter a different password.")
                form = ResetForm()
                return render(request, "restaurantReset.html", {'form': form})
            else:
                obj.password = form.cleaned_data['re_password']
                obj.save()
                request.session.flush()
                request.session.clear_expired()
                messages.success(request, "Password Reset Successfully.")
                return redirect('/restaurantLogin')
        else:
            request.session.flush()
            request.session.clear_expired()
            messages.error(request, "Reset Password Failed.\\nTry Again.")
            return redirect('/restaurantForgot')
    else:
        return restaurantForgot(request)

def deliveryLogin(request):
    if request.method == 'POST':
        form = DeliveryLoginForm(request.POST)
        if form.is_valid():
            pass
            if Delivery.objects.filter(delivery_id=form.cleaned_data['id']).exists():
                obj = Delivery.objects.get(delivery_id=form.cleaned_data['id'])
                if obj.password == form.cleaned_data['password']:
                    request.session['email'] = obj.email
                    messages.success(request, "Login Successful")
                    return redirect('/delivery')
                else:
                    messages.error(request, "Delivery Person ID and Password do not match.\\nTry Again.")
                    return redirect('/deliveryLogin')
            else:
                messages.error(request, "No delivery person account found for the given delivery person id.")
                return redirect('/deliveryLogin')
        else:
            messages.error(request, "Login Failed.")
            return redirect('/deliveryLogin')
    else:
        form = DeliveryLoginForm()
        return render(request, "deliveryLogin.html", {'form': form})

def deliveryMail(request, email, otp):
    obj = Delivery.objects.get(email=email)
    subject = "Reset Password"
    message = "Dear " + obj.name + ",\n\nWe received a request from you to reset the password for your Cloud Kitchen account that is associated with this email address.\n\nThe verification code is " + otp + ".\n\nPlease use the above OTP to complete your Reset Password request.\n\nIf you did not make this request, you can safely ignore this email.\n\nThank You,\nCloud Kitchen Team"
    to = [email]
    res = send_mail(subject, message, settings.EMAIL_HOST_USER, to)
    if res == 1:
        return True
    else:
        return False

def deliveryForgot(request):
    if request.method == 'POST':
        form = ForgotForm(request.POST)
        if form.is_valid():
            if Delivery.objects.filter(email=form.cleaned_data['email']).exists():
                global otp
                otp = str(randint(100000, 999999))
                if deliveryMail(request, form.cleaned_data['email'], otp):
                    request.session['delivery_email'] = form.cleaned_data['email']
                    return render(request, 'deliveryVerify.html')
                else:
                    messages.error(request, "Forgot Password Failed.")
                    return redirect('/deliveryForgot')
            else:
                messages.error(request, "No delivery person account found for the given email address.")
                return redirect('/deliveryForgot')
        else:
            messages.error(request, "Forgot Password Failed.")
            return redirect('/deliveryForgot')
    else:
        form = ForgotForm()
        return render(request, "deliveryForgot.html", {'form': form})

def deliveryVerify(request):
    if request.method == "POST":
        first = request.POST['first']
        second = request.POST['second']
        third = request.POST['third']
        fourth = request.POST['fourth']
        fifth = request.POST['fifth']
        sixth = request.POST['sixth']
        user_otp = first + second + third + fourth + fifth + sixth
        if user_otp == otp:
            form = ResetForm()
            return render(request, "deliveryReset.html", {'form': form})
        else:
            request.session.flush()
            request.session.clear_expired()
            messages.error(request, "Wrong OTP entered.\\nTry Again.")
            return redirect('/deliveryForgot')
    else:
        return deliveryForgot(request)

def deliveryReset(request):
    if request.method == "POST":
        form = ResetForm(request.POST)
        if form.is_valid():
            obj = Delivery.objects.get(email=request.session['delivery_email'])
            if obj.password == form.cleaned_data['re_password']:
                messages.error(request, "New Password is same as the Old Password.\\nPlease enter a different password.")
                form = ResetForm()
                return render(request, "deliveryReset.html", {'form': form})
            else:
                obj.password = form.cleaned_data['re_password']
                obj.save()
                request.session.flush()
                request.session.clear_expired()
                messages.success(request, "Password Reset Successfully.")
                return redirect('/deliveryLogin')
        else:
            request.session.flush()
            request.session.clear_expired()
            messages.error(request, "Reset Password Failed.\\nTry Again.")
            return redirect('/deliveryForgot')
    else:
        return deliveryForgot(request)

def browseRestaurant(request):
    obj2 = Restaurant.objects.filter(status=True)
    cuisines, cost_for_twos = {}, {}
    for i in obj2:
        cuisines[i.restaurant_id] = i.cuisine.strip("[]").replace("'", "")
        cost_for_twos[i.restaurant_id] = "Rs " + str(i.cost_for_two).split(".")[0] + " for two"
    return render(request, 'browse.html', {'obj': obj2, 'cuisines': cuisines, 'cost_for_twos': cost_for_twos})

def restaurantMenu(request, id):
    res = Restaurant.objects.get(restaurant_id=id)
    cuisines, cost_for_twos = res.cuisine.strip("[]").replace("'", ""), "Rs " + str(res.cost_for_two).split(".")[0] + " for two"
    obj1 = Category.objects.filter(restaurant=res)
    if not obj1.exists():
        obj1 = None
        return render(request, "browseRestaurantMenu.html", {'category_object': obj1, 'res': res})
    else:
        values = {}
        for i in obj1:
            temp = Item.objects.filter(category=i)
            for j in temp:
                if i.category in values:
                    values[i.category].append(j)
                else:
                    values[i.category] = [j]
        return render(request, "browseRestaurantMenu.html", {'category_object': obj1, 'res': res, 'item_object': values, 'cuisines': cuisines, 'cost_for_twos': cost_for_twos, 'range': range(1, 21)})