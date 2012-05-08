from django import forms
from mongoengine.django.auth import User

class UserDetailsForm(forms.Form):
    """
    A form that updates a user's First and Last Name, email address and other"
    optional details
    """
    first_name = forms.CharField(widget=forms.TextInput)
    last_name = forms.CharField(widget=forms.TextInput)
    email = forms.CharField(widget=forms.TextInput)

class UpdatePasswordForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
