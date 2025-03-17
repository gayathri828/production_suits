from django import forms
from django.contrib.auth.models import User
from .models import Customer

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'email', 'password',]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

class CustomerDetailsForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["first_name" ,'last_name', 'phone_number', 'address']
