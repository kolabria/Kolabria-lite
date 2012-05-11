from mongoengine.django.auth import User

from walls.models import Wall
from appliance.models import Box
from mongoforms import MongoForm
from django.forms.formsets import formset_factory
from django.utils.safestring import mark_safe 
from django import forms


class BoxForm(MongoForm):
    class Meta:
        document = Box
        fields = ('box_name', )

class EditBoxForm(forms.Form):
    box_name = forms.CharField(widget=forms.TextInput)


class ShareBoxForm(forms.Form):
    data = forms.CharField(widget=forms.TextInput(
                 attrs={'placeholder': 'BoxID or Box Name'}))

class UnsubWallForm(forms.Form):
    wid = forms.CharField(widget=forms.HiddenInput, required=False)


class PubWallForm(forms.Form):
    wid = forms.CharField(widget=forms.HiddenInput)


class NewBoxForm(forms.Form):
    box_id = forms.CharField(widget=forms.TextInput)
    box_name = forms.CharField(widget=forms.TextInput)

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


