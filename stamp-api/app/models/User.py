
from mongoengine import Document, StringField, EmailField, DateTimeField, BooleanField
from datetime import datetime

class User(Document):
    username = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    first_name = StringField()
    last_name = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    is_active = BooleanField(default=True)
    is_admin = BooleanField(default=False)

    meta = {
        'collection': 'users',
        'indexes': [
            'username',
            'email'
        ]
    }

    def __str__(self):
        return f"User(username={self.username}, email={self.email})"
