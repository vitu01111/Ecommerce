from flask import Blueprint, render_template, request, flash, redirect, url_for, session
 
from src.db import db
from src.Models.Product import Product
from src.Models.Category import Category
from src.Models.User import User
from src.Models.Image import Image
from src.Models.Order import Order
productOld_bp=Blueprint('productOld_bp',__name__)



@productOld_bp.route('/', methods=['GET'])
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
    return render_template('web/product/homePage.html', queryData=products,user=user,slider=slider_images)

# @product_bp.route('/newHomePage',methods=['GET'])
# def newHomePage():
#     return render_template('project1/newHomePage.html')


@productOld_bp.route('/details/<int:product_id>',methods=['GET'])
def details(product_id):
    products=db.session.query(Product).filter_by(id=product_id).first()
    
    # products=Product.query.get(product_id)

    return render_template('web/product/details.html',productt=products)



 

@productOld_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    # user_id = session.get('user_id')
    user_id=session['user_id']
    user = None
    if user_id:
        user = db.session.query(User).filter_by(id=user_id).first()
        if request.method == 'POST':
            new_username = request.form.get('username')
            # new_username=db.session.query(User).filter_by(id=user_id).first()
            if new_username and user:
                user.username = new_username
                db.session.commit()
                flash('Username updated successfully!', 'success')
                return redirect(url_for('productOld_bp.profile'))
    return render_template('web/product/profile.html', user=user)


@productOld_bp.route('/products', methods=['GET'])
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





 



 
 