from mongoengine import Document, StringField, ReferenceField, DateTimeField, IntField, FloatField
from datetime import datetime
from .User import User
from .Stamp import Stamp

class StampedPDF(Document):
    user = ReferenceField(User, required=True)
    stamp = ReferenceField(Stamp, required=True)
    pdf_path = StringField(required=True)
    output_path = StringField(required=True)
    x = IntField()
    y = IntField()
    scale = FloatField()
    page_number = IntField()
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'stamped_pdfs',
        'indexes': ['user', 'stamp']
    }