from mongoengine.django.auth import User

from walls.models import Wall
from appliance.models import Box

from django.forms.formsets import formset_factory
from django.utils.safestring import mark_safe 
from django import forms


class UnsubWallForm(forms.Form):
    wid = forms.CharField(widget=forms.HiddenInput, required=False)


class PubWallForm(forms.Form):
    wid = forms.CharField(widget=forms.HiddenInput)


class NewBoxForm(forms.Form):
    STATUS_CHOICES = (
        (u'Active', u'Active'),
        (u'New', u'Not Registered'),
        (u'Offline', u'Offline'),
    )
    name = forms.CharField(widget=forms.TextInput)
    location = forms.CharField(widget=forms.TextInput)
    status = forms.ChoiceField(widget=forms.Select,
                               choices=STATUS_CHOICES,
                               required=True)

class UpdateBoxForm(forms.Form):
    STATUS_CHOICES = (
        (u'Active', u'Active'),
        (u'New', u'Not Registered'),
        (u'Offline', u'Offline'),
    )
    name = forms.CharField(widget=forms.TextInput)
    location = forms.CharField(widget=forms.TextInput)
    status = forms.ChoiceField(widget=forms.Select,
                               choices=STATUS_CHOICES,
                               required=True)


class DelBoxForm(forms.Form):
    confirmed = forms.BooleanField(initial=False, required=True)


