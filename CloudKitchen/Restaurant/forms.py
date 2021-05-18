from django import forms

class ContactUsForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size': 100, 'class': 'common-input mb-20 form-control', 'placeholder': 'Enter Your Name', 'readonly':'readonly'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'common-input mb-20 form-control', 'placeholder': 'Enter Email Address', 'readonly':'readonly'}))
    subject = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'size': 50, 'class': 'common-input mb-20 form-control', 'placeholder': 'Enter Subject'}))
    message = forms.CharField(max_length=1000, min_length=50, widget=forms.Textarea(attrs={'size': 10, 'class': 'common-textarea form-control', 'placeholder': 'Enter Query', 'style': 'height: 202px;'}))

class CategoryForm(forms.Form):
    category = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'size': 50, 'class': 'input--style-1', 'placeholder': 'Category Name'}))

class CategoryItemForm(forms.Form):
    category = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'size': 50, 'class': 'input--style-1', 'placeholder': 'Category Name', 'readonly':'readonly'}))
    item = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'size': 50, 'class': 'input--style-1', 'placeholder': 'Item Name'}))
    price = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'input--style-1', 'placeholder': 'Price'}))

class ResetPasswordForm(forms.Form):
    old_password = forms.CharField(max_length=10, min_length=8, widget=forms.PasswordInput(attrs={'size': 10, 'class': 'form-control', 'placeholder': 'Old Password'}))
    password = forms.CharField(max_length=10, min_length=8, widget=forms.PasswordInput(attrs={'size': 10, 'class': 'form-control', 'placeholder': 'New Password'}))
    re_password = forms.CharField(max_length=10, min_length=8, widget=forms.PasswordInput(attrs={'size': 10, 'class': 'form-control', 'placeholder': 'Repeat New Password'}))

cuisines = (('North Indian', 'North Indian'), ('South Indian', 'South Indian'), ('Fast Food', 'Fast Food'), ('Beverages', 'Beverages'), ('Bakery', 'Bakery'), ('Desserts', 'Desserts'), ('Italian', 'Italian'), ('Chinese', 'Chinese'))
days = (('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday'))

class UpdateProfileForm(forms.Form):
    owner_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size': 100, 'class': 'input-text', 'placeholder': 'Owner Name'}))
    address = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size': 100, 'class': 'input-text', 'placeholder': 'Address / Locality'}))
    city = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'size': 20, 'class': 'input-text', 'placeholder': 'City'}))
    zip = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input-text', 'placeholder': 'Zip Code'}))
    restaurant_contact = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input-text', 'placeholder': 'Restaurant Contact Number'}))
    cost_for_two = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'input-text', 'placeholder': 'Cost for Two'}))
    outlets = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input-text', 'placeholder': 'Number of Outlets'}))