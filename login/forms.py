# -*- coding: utf-8 -*-
from django import forms
from mongoengine.django.auth import User


class UserCreationForm(forms.Form):
    """
    A form that creates a user, with no privileges, from the given username and password.
    """
    first_name = forms.CharField(label="First Name", max_length=30, required=False,
                       help_text="Enter your first name",
                       widget=forms.TextInput)
    last_name  = forms.CharField(label="Last Name", max_length=30, required=False,
                       help_text="Enter your last name",
                       widget=forms.TextInput)
    email = forms.EmailField(label="email", help_text = "Enter your email address. Email must be unique.",
                       error_messages = {'invalid': "This is not a valid email address"})
    company = forms.CharField(label="Company", max_length=30, widget=forms.TextInput)
    username = forms.RegexField(label="Username", max_length=30, regex=r'^[\w.@+-]+$',
        help_text = "Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.",
        error_messages = {'invalid': "This value may contain only letters, numbers and @/./+/-/_ characters."})
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput,
        help_text = "Enter the same password as above, for verification.")
    agree_terms = forms.BooleanField(widget=forms.CheckboxInput)

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError("A user with that email address already exists.")

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("A user with that username already exists.")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
