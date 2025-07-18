from flask import Blueprint, render_template, request, flash, redirect, url_for, session
 
from src.db import db
from src.Models.Product import Product
from src.Models.Category import Category
from src.Models.User import User
from src.Models.Image import Image
from src.Models.Order import Order,OrderDetail
product_bp=Blueprint('product_bp',__name__)



@product_bp.route('/', methods=['GET'])
def index():
    q = request.args.get('q', '')
    query = db.session.query(
        Product.id,
        Product.name,
        Product.image,
        Product.date,
        Product.price,
        Product.qty,
        Product.article,
        Product.country,
        Category.name.label('newCategoryName')
    ).join(Category, Category.id == Product.category_id)

    if q:
        query = query.filter(Product.name.ilike(f'%{q}%'))
    products = query.order_by(Product.id).all()
    slider_images=Image.query.limit(3).all()
    # slider_images = Image.query.limit(3).all()
    user = None
    if 'user_id' in session:
        
        # user = User.query.get(session['user_id'])when we have login already show can use this
        user = db.session.query(User).filter_by(id=session['user_id']).first()
    return render_template('web/index.html', queryData=products,user=user,slider=slider_images)

# @product_bp.route('/newHomePage',methods=['GET'])
# def newHomePage():
#     return render_template('project1/newHomePage.html')


@product_bp.route('/details/<int:product_id>',methods=['GET'])
def details(product_id):
    # category=db.session.query(Category).filter_by(id=).first()
    products=db.session.query(Product).filter_by(id=product_id).first()
    category = db.session.query(Category).filter_by(id=products.category_id).first()
   
    # products=Product.query.get(product_id)

    return render_template('web/detail.html',productt=products,category=category)


# @product_bp.route('/profile', methods=['GET', 'POST'])
# def profile():
#     # user_id = session.get('user_id')
#     user_id=session['user_id']
#     user = None
#     if user_id:
#         user = db.session.query(User).filter_by(id=user_id).first()
#         if request.method == 'POST':
#             new_username = request.form.get('username')
#             # new_username=db.session.query(User).filter_by(id=user_id).first()
#             if new_username and user:
#                 user.username = new_username
#                 db.session.commit()
#                 flash('Username updated successfully!', 'success')
#                 return redirect(url_for('product_bp.profile'))
#     return render_template('web/profile.html', user=user)


@product_bp.route('/products', methods=['GET'])
def products():
    q = request.args.get('q', '')
    query = db.session.query(
        Product.id,
        Product.name,
        Product.image,
        Product.date,
        Product.price,
        Product.qty,
        Product.article,
        Product.country,
        Category.name.label('newCategoryName')
    ).join(Category,Category.id == Product.category_id)
    if q:
        query = query.filter(Product.name.ilike(f'%{q}%'))
    products = query.order_by(Product.id).all()
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return render_template('web/product/products.html', products=products, user=user)

@product_bp.route('/ProcessCheckout')
def ProcessCheckout():
    return render_template('web/processCheckout.html', admins={})




# @product_bp.route('/historyUser/<int:user_id>')
# def history(user_id):
#     print(f"User ID: {user_id}")
#     user=db.session.query(User).filter_by(id=user_id).first()
#     orders=db.session.query(Order).filter_by(user_id=user_id).all()
#     return render_template('web/historyUser.html',orders=orders,user=user)





@product_bp.route('/orders/<int:product_id>',methods=['POST','GET'])
def add_order(product_id):
    add_product=db.session.query(Product).filter_by(id=product_id).first()
    return render_template('web/order.html',product=add_product)


@product_bp.route('/submitOrder/<int:product_id>',methods=['POST'])
def submitOrder(product_id):
    ProductObj=db.session.query(Product).filter_by(id=product_id).first()
    user_id=session['user_id']
    newOrder=Order(
        user_id=user_id,
        name=ProductObj.name,
        date=ProductObj.date,
        image=ProductObj.image,
        qty=1,
        price=ProductObj.price
    )
    db.session.add(newOrder)
    db.session.commit()
    return redirect(url_for('product_bp.index'))

# @product_bp.route('/historyUser')
# def history_self():
#     user_id = session.get('user_id')
#     if not user_id:
#         flash('Please log in to view your order history.', 'error')
#         return redirect(url_for('login.login'))
#     user = db.session.query(User).filter_by(id=user_id).first()
#     orders = db.session.query(Order).filter_by(user_id=user_id).all()
#     return render_template('web/historyUser.html', orders=orders, user=user)


@product_bp.route('/historyUser/<int:user_id>')
def history_self(user_id):
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to view your order history.', 'error')
        return redirect(url_for('login.login'))
    user = db.session.query(User).filter_by(id=user_id).first()
    orders = db.session.query(Order).filter_by(user_id=user_id).all()
    return render_template('web/historyUser.html', orders=orders, user=user)

@product_bp.route('/historyDetail/<int:order_id>',methods=['POST','GET'])
def historyDetail(order_id):
    # user_id=session.get('user_id') 
    # user=db.session.query(User).filter_by(id=user_id)
    orderDetail=db.session.query(OrderDetail).filter_by(order_id=str(order_id)).all()

    return render_template('/web/viewOrder.html',orderDetail=orderDetail)



@product_bp.route('/profile',methods=['GET','POST'])
def profile():
    user_id=session['user_id']
    user=None
    if user_id:
        user=db.session.query(User).filter_by(id=user_id).first()
        if request.method=='POST':
            new_username=request.form.get('username')
            if new_username and user:
                user.username=new_username
                db.session.commit()
                flash('username updated successfully','success')
                return redirect(url_for('product_bp.profile'))
    return render_template('web/profile.html',user=user)        





@product_bp.route('/contact',methods=['GET'])
def contact():
    return render_template('web/contact.html')


@product_bp.route('/product',methods=['GET'])
def productPage():
    query=db.session.query(
        Product.id,
        Product.name,
        Product.image,
        Product.date,
        Product.price,
        Product.qty,
        Product.article,
        Product.country,
        Category.name.label('newCategoryName')
    ).join(Category,Category.id==Product.category_id)
    products=query.order_by(Product.id).all()
    user_id=session.get('user_id')
    user=None
    if user_id in session:
        user=db.session.query(User).filter_by(id=user_id).first()
    return render_template('web/product.html',queryData=products,user=user)


@product_bp.route('/sport',methods=['GET'])
def sport():
    return render_template('web/sport.html')




