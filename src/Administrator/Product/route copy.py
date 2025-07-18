from flask import Flask,Blueprint,redirect,render_template,url_for,request
from src.Models.Product import Product
from src.Models.Category import Category
from src.db import db
from datetime import datetime
import os
# from assets.static.uploads import assets 

# from models import Category,Products,app
from werkzeug.utils import secure_filename
prdouct_bp=Blueprint('prdouctt_bp',__name__)

UPLOAD_FOLDER='static/uploads'
ALLOWED_EXTENSIONS={'png','jpg','jpeg','gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

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
    newCategories=Category.query.all()
    # newCategories=db.session.query(Category).all()
    return render_template('admin/product/product_add.html',newCategories=newCategories) 
@prdouct_bp.route('/createForm', methods=['POST'])
def createProductFormData(): 
    name = request.form['name']
    category_id = int(request.form['category_id']) if request.form['category_id'] else 1
    price = float(request.form['price'])
    qty = int(request.form['qty'])
    date = datetime.strptime(request.form['date'], '%Y-%m-%d')
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
   
@prdouct_bp.route('/editForm/<int:product_id>',methods=['GET'])
def editProductForm(product_id):
    product=Product.query.get_or_404(product_id)
    newCategory=Category.query.all()
    return render_template('admin/product/product_edit.html',edit_pro=product,edit_cat=newCategory)

@prdouct_bp.route('/editForm/<int:product_id>',methods=['POST'])
def editProductFormData(product_id):
    product=Product.query.get_or_404(product_id)
    if product:
        product.name=request.form['name']
        product.category_id=int(request.form['category_id']) if 'category_id' in request.form else 1
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

@prdouct_bp.route('/delete/<int:delete_id>',methods=['POST'])
def deleteProduct(delete_id):
    product=Product.query.get_or_404(delete_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('prdouctt_bp.products_list'))