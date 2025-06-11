from mongoengine import Document, StringField, ReferenceField, DateTimeField
from datetime import datetime
from .User import User

class Stamp(Document):
    user = ReferenceField(User, required=True)
    file_path = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    description = StringField()

    meta = {
        'collection': 'stamps',
        'indexes': ['user']
    }