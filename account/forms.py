from mongoengine.django.auth import User
from django import forms

class NewAccountForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
                           attrs={'placeholder': 'username',
                                  'class': 'span4'}),
                           max_length=30, 
                           required=True)
    first_name = forms.CharField(widget=forms.TextInput(
                           attrs={'placeholder': 'First Name',
                                  'class': 'span4'}),
                           max_length=30, 
                           required=True)
    last_name = forms.CharField(widget=forms.TextInput(
                           attrs={'placeholder': 'Last Name',
                                  'class': 'span4'}),
                           max_length=30, 
                           required=True)
    email = forms.EmailField(widget=forms.TextInput(
                           attrs={'placeholder': 'first.last@company.com',
                                  'class': 'span4'}),
                           max_length=30,
                           required=True)
    company = forms.CharField(widget=forms.TextInput(
                           attrs={'placeholder': 'Company',
                                  'class': 'span4'}),
                           max_length=30, 
                           required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(
                           attrs={'placeholder': '**********',
                                  'class': 'span4'}),
                           max_length=30, 
                           required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(
                           attrs={'placeholder': '**********',
                                  'class': 'span4'}),
                           max_length=30, 
                           required=True)
#    agree_terms = forms.BooleanField(widget=forms.CheckboxInput)


class JoinMeetingForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
                           attrs={'placeholder': 'Your Name',
                                  'class': 'span4'}),
                           max_length=30,
                           required=True)
    room = forms.CharField(widget=forms.TextInput(
                           attrs={'placeholder': 'Case Insensitive',
                                  'class': 'span4'}),
                           max_length=30,
                           required=True)
    code = forms.CharField(widget=forms.TextInput(
                           attrs={'placeholder': '4-digit secret code',
                                  'class': 'span4'}),
                           max_length=30,
                           required=True)

