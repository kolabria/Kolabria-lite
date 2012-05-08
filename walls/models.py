from django.core.exceptions import ObjectDoesNotExist, ValidationError

from mongoengine import connect, Document
from mongoengine import ReferenceField, StringField, DateTimeField
from mongoengine import EmailField, ListField, ObjectIdField

from mongoengine.django.auth import User
from kolabria.account.models import Account
from kolabria.appliance.models import Box
from datetime import datetime
from django import forms

class Wall(Document):
    """
    Wall model in MongoDB to represent Wall objects
    """
    STATUS_CHOICES = (
        (u'Active', u'Active'),
        (u'Private', u'Private'),
        (u'Inactive', u'Inactive'),
    )        
    company = ReferenceField(Account)
    owner = ReferenceField(User)
    name = StringField(max_length=32, required=True)
    description = StringField(max_length=256, required=False)
    status = StringField(default='Active', 
                         max_length=8, 
                         choices=STATUS_CHOICES,
                         required=True)
    created = DateTimeField(default=datetime.now(), required=False)
    modified = DateTimeField(default=datetime.now(), required=True)
    published = ListField(StringField())
    sharing = ListField(EmailField())
    viewing = ListField(EmailField())


    def __unicode__(self):
        """
        Returns the Wall Name as unicode description for admin and shell
        """
        return self.name

    def clean(self):
        # check appliance_id is valid before appending id to Wall.published 
        for id in published:
            if not Box.objects.get(id=id):
                raise ValidationError('Invalid Appliance_id: %s' % id)
