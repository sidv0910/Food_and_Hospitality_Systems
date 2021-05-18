from django import forms

class ContactUsForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size': 100, 'class': 'common-input mb-20 form-control', 'placeholder': 'Enter Your Name', 'readonly':'readonly'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'common-input mb-20 form-control', 'placeholder': 'Enter Email Address', 'readonly':'readonly'}))
    subject = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'size': 50, 'class': 'common-input mb-20 form-control', 'placeholder': 'Enter Subject'}))
    message = forms.CharField(max_length=1000, min_length=50, widget=forms.Textarea(attrs={'size': 10, 'class': 'common-textarea form-control', 'placeholder': 'Enter Query', 'style': 'height: 202px;'}))

class UpdateProfileForm(forms.Form):
    contact = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'mb-4', 'placeholder': 'Contact Number'}))
    address = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size': 100, 'class': 'mb-4', 'placeholder': 'Address'}))