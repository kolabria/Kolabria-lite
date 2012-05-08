from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models.signals import post_save

from mongoengine import connect, Document
from mongoengine import ReferenceField, StringField, DateTimeField
from mongoengine import EmailField, ListField, ObjectIdField

from mongoengine.django.auth import User
from kolabria.account.models import Account
from kolabria.appliance.models import Box
from datetime import datetime
from django import forms

class UserProfile(Document):
    """
    User Profile model in MongoDB to represent User Details objects
    """
    STATUS_CHOICES = (
        (u'Active', u'Active'),
        (u'Inactive', u'Inactive'),
        (u'Deleted', u'Deleted'),
    )
    user = models.OneToOneField(User)
    company = ReferenceField(Account)
    phone = StringField(max_length=30, required=False)
    description = StringField(max_length=256, required=False)
    status = StringField(default='Active', max_length=8,
                         choices=STATUS_CHOICES, required=True)

    def __unicode__(self):
        """
        Returns the Wall Name as unicode description for admin and shell
        """
        if user.first_name:
            return '%s %s' % (user.first_name, user.last_name)
        else:
            return user.username

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
