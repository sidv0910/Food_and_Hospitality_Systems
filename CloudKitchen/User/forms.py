from django import forms

class ContactUsForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size': 100, 'class': 'common-input mb-20 form-control', 'placeholder': 'Enter Your Name', 'readonly':'readonly'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'common-input mb-20 form-control', 'placeholder': 'Enter Email Address', 'readonly':'readonly'}))
    subject = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'size': 50, 'class': 'common-input mb-20 form-control', 'placeholder': 'Enter Subject'}))
    message = forms.CharField(max_length=1000, min_length=50, widget=forms.Textarea(attrs={'size': 10, 'class': 'common-textarea form-control', 'placeholder': 'Enter Query', 'style': 'height: 202px;'}))

class UpdateProfileForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size': 100, 'class': 'form-control', 'placeholder': 'Name'}))
    contact = forms.IntegerField(widget=forms.NumberInput(attrs={'min':6000000000, 'max':9999999999, 'class': 'form-control', 'placeholder': 'Contact Number'}))

class AddressForm(forms.Form):
    line1 = forms.CharField(max_length=100, min_length=5, widget=forms.TextInput(attrs={'size': 100, 'class': 'form-control', 'placeholder': 'Line 1'}))
    line2 = forms.CharField(max_length=100, min_length=5, widget=forms.TextInput(attrs={'size': 100, 'class': 'form-control', 'placeholder': 'Line 2'}))
    landmark = forms.CharField(max_length=50, min_length=5, widget=forms.TextInput(attrs={'size': 50, 'class': 'form-control', 'placeholder': 'Landmark'}))
    locality = forms.CharField(max_length=50, min_length=5, widget=forms.TextInput(attrs={'size': 50, 'class': 'form-control', 'placeholder': 'Locality'}))
    city = forms.CharField(max_length=20, min_length=5, widget=forms.TextInput(attrs={'size': 20, 'class': 'form-control', 'placeholder': 'City'}))
    zip = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 100000, 'max': 999999, 'class': 'form-control', 'placeholder': 'Zip'}))