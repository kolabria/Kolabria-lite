from mongoengine import connect, Document
from mongoengine import ReferenceField, StringField, DateTimeField, ListField
from mongoengine import ObjectIdField
from mongoengine.django.auth import User

from account.models import Account
from datetime import datetime

class Box(Document):
    """
    Box represents a unique WikiWall appliance
    """
    company = ReferenceField(Account)
    owner = ReferenceField(User)
    name = StringField(default='New Appliance', max_length=32, required=True)
    location = StringField(max_length=100, required=False)
    active_wall = StringField(required=False)
    walls = ListField(StringField())

    def __unicode__(self):
        return self.name
