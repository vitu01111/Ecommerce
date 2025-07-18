 
from flask import request, redirect, url_for, session, flash, render_template, Blueprint
from src.db import db 
from src.Models.Order import Order
from datetime import date
from src.Models.Product import Product

order_router = Blueprint('order', __name__)
 
 
@order_router.route('/order/<int:product_id>', methods=['POST','GET'])
def add_order(product_id):
     
    ProductObj = db.session.query(Product).filter_by(id=product_id).first()
    return render_template('web/product/order.html',product=ProductObj)
    
 
@order_router.route('/historyUser/<int:user_id>')
def history(user_id):
    q = request.args.get('q', '')
    if q:
        orders = db.session.query(Order).filter(
            Order.user_id == user_id,
            Order.name.ilike(f'%{q}%')
        ).all()
    else:
      
        orders = db.session.query(Order).filter_by(user_id=user_id).all()
    return render_template('/web/historyUser.html', orders=orders, user_id=user_id)




@order_router.route('/historyDetail/<int:user_id>',methods=['POST','GET'])
def historyDetail(user_id):
    orderDetail=db.session.query(orderDetail).filter_by(id=user_id)
    return render_template('/web/viewOrder.html',orderDetail=orderDetail)



# @order_router.route('/history/<int:user_id>',methods=['POST','GET'])
# def historyUser(user_id):
#     user_id=session.get('user_id')
#     user=None
#     if user_id:
#         user=db.session.query(Order).filter_by(user_id=user_id)
        
#     order=db.session.query(Order).filter_by(id=user_id).filter()
#     return render_template('web/product/order.html',product=order)
    

@order_router.route('/submit/<product_id>', methods=['POST'])
def submit_order(product_id):
    ProductObj = db.session.query(Product).filter_by(id=product_id).first()
    user_id = session['user_id']
    itemOrder = Order(
        user_id=user_id,
        name=ProductObj.name,
        
        date=ProductObj.date,
        image=ProductObj.image,
        qty=1,
        price=ProductObj.price
    )
    db.session.add(itemOrder)
    db.session.commit()
     
    # return redirect(url_for('order.history', user_id=user_id))
    return redirect(url_for('productOld_bp.index'))



