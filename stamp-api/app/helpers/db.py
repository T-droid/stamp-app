from mongoengine import connect

def init_db():
    connect(
        db="pdf-stamper",
        alias="default",
        host="mongodb://localhost:27017/pdf-stamper"
    )