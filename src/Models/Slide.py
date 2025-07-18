from src.db import db 

class Slider(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(100),nullable=False)
    image=db.Column(db.String(255),nullable=True)
   