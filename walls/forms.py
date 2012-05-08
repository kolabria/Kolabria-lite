from mongoengine.django.auth import User

from walls.models import Wall
from appliance.models import Box

from django.forms.formsets import formset_factory
from django.utils.safestring import mark_safe 
from django import forms


class NewWallForm(forms.Form):
    OPTIONS = ()
    name = forms.CharField(widget=forms.TextInput(
                           attrs={'placeholder': 'Name this Wikiwall',
                                  'class': 'span4'}),
                           max_length=30, 
                           required=True)

    placeholder = 'steve.jobs@apple.com, jimi.hendrix@rocknroll.com, '
    placeholder += 'santa.clause@northpole.ca, etc ...'
    invited = forms.CharField(widget=forms.Textarea(
                                  attrs={'placeholder': placeholder,
                                         'class': 'span8'}),
                              required=False)
    all_boxes = Box.objects.all()
    for box in all_boxes:
        OPTIONS += ( box.id, box.name ),
    publish = forms.MultipleChoiceField(
                       widget=forms.SelectMultiple(
                                      attrs={'class': 'span4'}),
                       choices=OPTIONS,
                       required=False)

#    def clean_name(self):
#        try:
#            exists = Wall.objects.filter(name=name))
#        except real.DoesNotExist:
#            return self.cleaned_data['invited'] 
#        raise forms.ValidationError(invited)
#        raise forms.ValidationError("Sorry, %s is not a valid user. Please try again" % invited)

class DeleteWallForm(forms.Form):
    confirmed = forms.BooleanField(initial=False, required=True)


class PubWallForm(forms.Form):
    OPTIONS = ()
    all_boxes = Box.objects.all()
    for box in all_boxes:
        box_title = '%s - %s' % (box.name, box.location)
        OPTIONS += ( box.id, box_title ),
    publish = forms.MultipleChoiceField(
                       widget=forms.SelectMultiple(
                                      attrs={'class': 'controls span4'}),
                       choices=OPTIONS,
                       required=False)


class UnpubWallForm(forms.Form):
    box_id = forms.CharField(widget=forms.HiddenInput, required=False)


class ShareWallForm(forms.Form):
    shared = forms.EmailField(widget=forms.TextInput(
                              attrs={'placeholder': 'email@address.com'}), 
                              max_length=60, required=True)


class UnshareWallForm(forms.Form):
    unshared = forms.BooleanField(widget=forms.CheckboxInput,
                                  label='Unshare')
                                  
    email = forms.EmailField(widget=forms.HiddenInput)

class UpdateWallForm(forms.Form):
    OPTIONS = () # Publish to Appliances
    name = forms.CharField(widget=forms.TextInput(
                           attrs={'class': 'span8'}), 
                           max_length=30, required=True)
    invited = forms.EmailField(widget=forms.TextInput(
                               attrs={'placeholder':'email@address.com',
                                      'class': 'span8'}),
                               required=False)

#    def clean_invited(self):
#        invited = self.cleaned_data['invited']
#        try:
#            real = User.objects.filter(email=invited)
#        except real.DoesNotExist:
#            return self.cleaned_data['invited'] 
#        raise forms.ValidationError(invited)
#        raise forms.ValidationError("Sorry, %s is not a valid user. Please try again" % invited)
