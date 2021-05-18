from django import forms
from .models import User

class RegisterForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size':100, 'class': 'form-control', 'placeholder': 'Full Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    contact = forms.IntegerField(widget=forms.NumberInput(attrs={'min':6000000000, 'max':9999999999, 'class': 'form-control', 'placeholder': 'Contact Number'}))
    password = forms.CharField(max_length=10, min_length=8, widget=forms.PasswordInput(attrs={'size':10, 'class': 'form-control', 'placeholder': 'Password'}))
    re_password = forms.CharField(max_length=10, min_length=8, widget=forms.PasswordInput(attrs={'size':10, 'class': 'form-control', 'placeholder': 'Repeat Password'}))

    def clean(self):
        cd = self.cleaned_data
        if User.objects.filter(email=cd.get("email")).exists():
            raise forms.ValidationError("A user account with the given email address exists.\\nTry another email address.")
        if User.objects.filter(contact=cd.get("contact")).exists():
            raise forms.ValidationError("A user account with the given email contact number exists.\\nTry another contact number.")

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    password = forms.CharField(max_length=10, min_length=8, widget=forms.PasswordInput(attrs={'size': 10, 'class': 'form-control', 'placeholder': 'Password'}))

class ForgotForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))

class ResetForm(forms.Form):
    password = forms.CharField(max_length=10, min_length=8, widget=forms.PasswordInput(attrs={'size': 10, 'class': 'form-control', 'placeholder': 'New Password'}))
    re_password = forms.CharField(max_length=10, min_length=8, widget=forms.PasswordInput(attrs={'size': 10, 'class': 'form-control', 'placeholder': 'Repeat New Password'}))

class ContactUsForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size': 100, 'class': 'common-input mb-20 form-control', 'placeholder': 'Enter Your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'common-input mb-20 form-control', 'placeholder': 'Enter Email Address'}))
    subject = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'size': 50, 'class': 'common-input mb-20 form-control', 'placeholder': 'Enter Subject'}))
    message = forms.CharField(max_length=1000, min_length=50, widget=forms.Textarea(attrs={'size': 10, 'class': 'common-textarea form-control', 'placeholder': 'Enter Query', 'style': 'height: 202px;'}))

cuisines = (('North Indian', 'North Indian'), ('South Indian', 'South Indian'), ('Fast Food', 'Fast Food'), ('Beverages', 'Beverages'), ('Bakery', 'Bakery'), ('Desserts', 'Desserts'), ('Italian', 'Italian'), ('Chinese', 'Chinese'))
days = (('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday'))

class PartnerForm(forms.Form):
    restaurant_name = forms.CharField(max_length=100, error_messages={'required':"Please Enter your Name"}, widget=forms.TextInput(attrs={'size': 100, 'class': 'form-control', 'placeholder': 'Restaurant Name'}))
    owner_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size': 100, 'class': 'input-text', 'placeholder': 'Owner Name'}))
    address = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size': 100, 'class': 'input-text', 'placeholder': 'Address / Locality'}))
    city = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'size': 20, 'class': 'input-text', 'placeholder': 'City'}))
    zip = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input-text', 'placeholder': 'Zip Code'}))
    restaurant_email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input-text', 'placeholder': 'Restaurant Email Address'}))
    restaurant_contact = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input-text', 'placeholder': 'Restaurant Contact Number'}))
    password = forms.CharField(max_length=10, widget=forms.PasswordInput(attrs={'size': 10, 'class': 'input-text', 'placeholder': 'Password'}))
    cost_for_two = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'input-text', 'placeholder': 'Cost for Two'}))
    outlets = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input-text', 'placeholder': 'Number of Outlets'}))
    cuisine = forms.MultipleChoiceField(required=True, choices=cuisines, widget=forms.CheckboxSelectMultiple())
    working_days =forms.MultipleChoiceField(required=True, choices=days, widget=forms.CheckboxSelectMultiple())
    shop_license = forms.FileField(widget=forms.FileInput(attrs={'class': 'input-text', 'accept': '.pdf'}))
    fssai = forms.FileField(widget=forms.FileInput(attrs={'class': 'input-text', 'accept': '.pdf'}))
    gstin_pan = forms.FileField(widget=forms.FileInput(attrs={'class': 'input-text', 'accept': '.pdf'}))
    menu = forms.FileField(widget=forms.FileInput(attrs={'class': 'input-text', 'accept': '.pdf'}))
    facade = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    kitchen = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    dining_packaging = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    locality = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

class RestaurantLoginForm(forms.Form):
    restaurant_id = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'size':6, 'class': 'form-control', 'placeholder': 'Restaurant ID'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    password = forms.CharField(max_length=10, min_length=8, widget=forms.PasswordInput(attrs={'size': 10, 'class': 'form-control', 'placeholder': 'Password'}))

class DeliveryLoginForm(forms.Form):
    id = forms.CharField(max_length=6, min_length=6, widget=forms.TextInput(attrs={'size': 8, 'class': 'form-control', 'placeholder': 'Delivery Person ID'}))
    password = forms.CharField(max_length=10, min_length=8, widget=forms.PasswordInput(attrs={'size': 10, 'class': 'form-control', 'placeholder': 'Password'}))