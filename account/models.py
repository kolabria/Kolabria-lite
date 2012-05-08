from mongoengine import connect, Document
from mongoengine import ReferenceField, StringField, EmailField
from mongoengine import DateTimeField, ListField
from mongoengine.django.auth import User
from datetime import datetime

class Account(Document):
    """
    Corporate Account model in MongoDB to represent Company objects
    """
    admin = ReferenceField(User)
    company = StringField(max_length=32)

    def __unicode__(self):
        """
        Returns the Wall Name as unicode description for admin and shell
        """
        return self.company
