from django.core.exceptions import ObjectDoesNotExist, ValidationError

from mongoengine import connect, Document
from mongoengine import ReferenceField, StringField, DateTimeField
from mongoengine import EmailField, ListField, ObjectIdField, IntField

from mongoengine.django.auth import User
from account.models import Account
from appliance.models import Box
from datetime import datetime
from django import forms
from random import randint


def generate_code():
    code = randint(1000,9999)
    return code


class Wall(Document):
    """
    Wall model in MongoDB to represent Wall objects
    """
    company = ReferenceField(Account)
    box_id = StringField(max_length=30)
    code = IntField(default=generate_code, required=True)
    published = ListField(StringField())


    def __unicode__(self):
        """
        Returns the Wall Name as unicode description for admin and shell
        """
        return self.box_id

    def clean(self):
        # check appliance_id is valid before appending id to Wall.published 
        for id in published:
            if not Box.objects.get(id=id):
                raise ValidationError('Invalid Appliance_id: %s' % id)
