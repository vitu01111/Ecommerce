
from src.db import db 

#product
class Product(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(100),nullable=False)
    category_id=db.Column(db.Integer,db.ForeignKey('category.id'),nullable=False)
    image=db.Column(db.String(255),nullable=True)
    date=db.Column(db.Date,nullable=False)
    price=db.Column(db.Float,nullable=False)
    qty=db.Column(db.Integer,nullable=False)
    article=db.Column(db.Text,nullable=True)
    country=db.Column(db.String(100),nullable=False)
   
    
