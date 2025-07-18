from src.db import db

class Image(db.Model):
 
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    image=db.Column(db.String(255),nullable=True)

