from flask import Flask,Blueprint,current_app,redirect,render_template,url_for,request,session,flash
from src.Models.Product import Product
from src.Models.Category import Category
from src.db import db
from datetime import datetime
import os
from src.Models.User import User
from src.Administrator.Product.form import ProductForm

# from assets.static.uploads import assets 

# from models import Category,Products,app
from werkzeug.utils import secure_filename
prdouct_bp=Blueprint('prdouctt_bp',__name__)

UPLOAD_FOLDER='static/uploads'
ALLOWED_EXTENSIONS={'png','jpg','jpeg','gif','avif','webp','gif','svg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS



@prdouct_bp.before_request
def require_admin_login():
    if 'admin_id' not in session:
        flash('You must be logged in as admin to access this page.', 'danger')
        return redirect(url_for('auth.login'))

@prdouct_bp.route('/',methods=['GET'])
def products_list():
    q=request.args.get('q','')
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
    ).outerjoin(Category,Category.id== Product.category_id)
    if q:
        query=query.filter(Product.name.ilike(f'%{q}%'))
    products=query.order_by(Product.id).all()

    return render_template('admin/product/product_list.html', products=products)


@prdouct_bp.route('/createform',methods=['GET'])
def createProductForm():
    form =ProductForm()
    newCategories=Category.query.all()
    return render_template('admin/product/product_add.html',newCategories=newCategories,form=form) 
@prdouct_bp.route('/createForm', methods=['POST'])
def createProductFormData(): 
    form =ProductForm()
    if form.validate_on_submit():
        name = request.form['name']
        category_id = int(request.form['category_id']) if request.form['category_id'] else 1
        price = float(request.form['price']) if request.form['price'] else 0
        qty = int(request.form['qty']) if request.form['qty'] else 0
        date = datetime.strptime(request.form['date'], '%Y-%m-%d') if request.form['date'] else datetime.now()
        article = request.form['article']
        country = request.form['country']
        image_file = request.files.get('image')
        image_filename = ""  # Set your default image filename here

        if image_file and image_file.filename:
            if allowed_file(image_file.filename):
                image_filename = secure_filename(image_file.filename)
                image_path = os.path.join(UPLOAD_FOLDER, image_filename)     
                image_file.save(image_path)

        new_product = Product(
            name=name,
            category_id=category_id,
            price=price,
            qty=qty,
            date=date,
            article=article,
            country=country,
            image=image_filename
        )
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('prdouctt_bp.products_list')) 
    else:
        # If validation fails, re-render the form with errors
        return render_template('admin/product/product_add.html', form=form)
    
@prdouct_bp.route('/editForm/<int:product_id>',methods=['GET'])
def editProductForm(product_id):
 
    product=Product.query.get_or_404(product_id)
    form =ProductForm(obj=product)
    newCategory=Category.query.all()
    return render_template('admin/product/product_edit.html',edit_pro=product,edit_cat=newCategory,form=form)

@prdouct_bp.route('/editForm/<int:product_id>',methods=['POST'])
def editProductFormData(product_id):
    product=Product.query.get_or_404(product_id)
    if product:
        product.name=request.form['name']
        category_id = request.form.get('category_id')
        product.category_id = int(category_id) if category_id and category_id.isdigit() else 1
        product.price=float(request.form['price'])
        product.qty=int(request.form['qty'])
        product.date=datetime.strptime(request.form['date'],'%Y-%m-%d')
        product.article=request.form['article']
        product.country=request.form['country']
        image_file=request.files.get('image')
        if image_file and image_file.filename and allowed_file(image_file.filename):
            image_filename=secure_filename(image_file.filename)
            image_path=os.path.join(UPLOAD_FOLDER,image_filename)
            image_file.save(image_path)
            product.image=image_filename
        db.session.commit()
        return redirect(url_for('prdouctt_bp.products_list'))
    return "Edit not found",404

@prdouct_bp.route('/delete/<int:delete_id>',methods=['GET'])
def deleteProduct(delete_id):
    product=Product.query.get_or_404(delete_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('prdouctt_bp.products_list'))



# @prdouct_bp.route('/profileAdmin', methods=['GET', 'POST'])
# def profileAdmin():
#     userAdmin = db.session.query(User).first()

#     if request.method == 'POST':
#         username = request.form.get('username')
#         gmail = request.form.get('gmail')
#         image = request.files.get('image')

#         if username:
#             userAdmin.username = username

#         if gmail:
#             userAdmin.email = gmail

#         if image and allowed_file(image.filename):
#             filename = secure_filename(image.filename)
#             uploads = os.path.join(current_app.root_path, UPLOAD_FOLDER)
#             os.makedirs(uploads, exist_ok=True)
#             image.save(os.path.join(uploads, filename))
#             userAdmin.image = filename

#         db.session.commit()
#         flash('Profile updated successfully', 'success')
#         return redirect(url_for('prdouctt_bp.profileAdmin'))

#     return render_template('admin/profile.html', userAdmin=userAdmin)





 