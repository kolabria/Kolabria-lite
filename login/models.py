from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models.signals import post_save

from mongoengine import connect, Document
from mongoengine import ReferenceField, StringField, DateTimeField
from mongoengine import EmailField, ListField, ObjectIdField

from mongoengine.django.auth import User
from account.models import Account
from appliance.models import Box
from datetime import datetime
from django import forms

class UserProfile(Document):
    """
    User Profile model in MongoDB to represent User Details objects
    """
    username = StringField(max_length=32, required=True)
    user = ReferenceField(User)
    company = ReferenceField(Account)
