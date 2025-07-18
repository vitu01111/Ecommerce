from src.db import db
 
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    paymentMethod=db.Column(db.String, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.String)
    

class OrderDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String, nullable=False)
    product_id = db.Column(db.String, nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.Text, nullable=False)
    categoryName = db.Column(db.String, nullable=False)

    