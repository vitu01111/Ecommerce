from flask import Blueprint,request,session
from src.Models.Company import Company
from src.db import db
from src.Models.Product import Product
from src.Models.Category import Category
from src.Models.Order import Order, OrderDetail
from src.Models.User import User

from datetime import datetime, date

order_api=Blueprint('order_api',__name__)
@order_api.route('/submit',methods=['GET'])
def index():
    return "order api "

@order_api.route('/submitOrder',methods=['POST'])
def submit():
    try:
        data=request.get_json()
        requestItems = data.get("items", [])
        requestTotalPrice = data.get("totalPrice", 0)
        requestPaymentMethod = data.get("paymentMethod")
        print(f"data is {requestItems}")
        current_datetime = datetime.now()
        
        OrderItem=Order(
            user_id=session.get("user_id"),  # get user_id from session
            date=current_datetime,
            total_price=requestTotalPrice,
            created_at=current_datetime,
            paymentMethod=requestPaymentMethod
        )   
        db.session.add(OrderItem)
        db.session.commit()
        
        
        for item in requestItems:
            
            orderDetail=OrderDetail(
                order_id=OrderItem.id,  # Assuming OrderItem has an id attribute
                product_id=item.get("id"),
                product_name=item.get("name"),
                qty=item.get("qty"),
                price=item.get("price"),
                image=item.get("image"),
                categoryName = item.get("categoryName")
            )
            db.session.add(orderDetail)
            db.session.commit()

        return {"status": True, "Message": "order api succeessfully","orderID":OrderItem.id}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"status": False, "Message": "An error occurred while processing the order","orderID":''}, 500


@order_api.route('/submitest',methods=['get'])
def indextest():
    data=request.get_json()
    if data:
        print(f"data is {data}")
    else:
        print("not fond data")    
    return "order api successfully "
@order_api.route('/submitest2',methods=['POST'])
def indextest2():
    data=request.get_json()
    for item in data:
        items=Company(
            id=item.get("id"),
            name=item.get("name"),
            address=item.get("address"),
            email=item.get("email"),
            phone=item.get("PhoneNumber"),
            description=item.get("description")
        )
        db.session.add(items)
        db.session.commit()
        print(f"item is {data}")
    
    return "order api successfully 2"
@order_api.route('/submitProduct',methods=['POST'])
def submitProduct():
    data=request.get_json()
    for item in data:
        items=Product(
        id=item.get("id"),
        name=item.get("Prodcut_name"),
        category_id=item.get("category_id"),
        image=item.get("image"),
        date=item.get("date"),
        price=item.get("price"),
        qty=item.get("qty"),
        article=item.get("article"),
        country=item.get("country")

        )
        db.session.add(items)
        db.session.commit()
        print(f"product is {data}")
        return "Product added successfully"
    




# @order_api.route('/submitOrder', methods=['POST'])
# def submitOrder():
#     order = request.get_json()
#     print(f"order is {order}")
#     for item in order:
#         user_id = item.get("user_id")
#         user = db.session.query(User).filter_by(id=user_id).first()
#         if not user:
#             return f"User with id {user_id} does not exist", 400
#         items = Order(
#             id=item.get("id"),
#             user_id=user_id,
#             name=item.get("name"),
#             date=item.get("date"),
#             image=item.get("image"),
#             qty=item.get("qty"),
#             price=item.get("price"),
#             created_at=item.get("created_at")
#         )
#         db.session.add(items)
#         db.session.commit()
#         print(f"order is {order}")
#     return "Order added successfully"




#  for item in order:
#          items=Order(
#          id=item.get("id"),
#          user_id=item.get("user_id")
#          name=item.get("name"),
#          date=item.get("date"),
#          image=item.get("image"),
#          qty=item.get("qty"),
#          price=item.get("price")
#          created_at=item.get("created_at")
#         )
    #     class Order(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # name = db.Column(db.String(100), nullable=False)
    # date = db.Column(db.Date, nullable=False)
    # image = db.Column(db.String(255), nullable=False)
    # qty = db.Column(db.Integer, nullable=False)
    # price = db.Column(db.Float, nullable=False)
    # created_at = db.Column(db.DateTime, default=datetime.utcnow)
