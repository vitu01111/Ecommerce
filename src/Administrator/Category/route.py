# from models import db,app,NewCategory
from flask import Flask,Blueprint,render_template,request,redirect,url_for,jsonify,session,flash
from src.Models.Category import Category 
from src.Administrator.Category.form import CagegoryForm
from src.db import db


category_bp=Blueprint('category',__name__)

@category_bp.before_request
def require_admin_login():
    if 'admin_id' not in session:
        # flash('You must be logged in as admin to access this page.', 'danger')
        return redirect(url_for('auth.login'))

@category_bp.route('/',methods=['GET'])
def category_list():
    newcategoryy=Category.query.order_by(Category.id).all()
    return render_template('admin/category/category_list.html',newcategory=newcategoryy)

@category_bp.route('/createForm',methods=['GET'])
def createNewCategoryForm():
    form = CagegoryForm()
    return render_template('admin/category/category_add.html',form=form)

@category_bp.route('/insertcategory',methods=['POST'])
def insertNewCategory():
    newname=request.form['name']
    new_category=Category(name=newname)
    db.session.add(new_category)
    db.session.commit()
    return redirect(url_for('category.category_list'))
@category_bp.route('/editForm/<int:newCategory_id>',methods=['GET'])
def editNewCategoryForm(newCategory_id):
    # GetNewCategory=Category.query.get_or_404(newCategory_id)
    GetNewCategory = db.session.query(Category).filter_by(id=newCategory_id).first()
    form = CagegoryForm(obj=GetNewCategory)
    return render_template('admin/category/category_edit.html',form=form,GetNewCategory=GetNewCategory)
@category_bp.route('/editFormData/<int:newCategory_id>',methods=['POST'])
def editNewCategoryFormData(newCategory_id):
    GetNewCategory=Category.query.get_or_404(newCategory_id)
    if GetNewCategory:
        newName=request.form['name']
        GetNewCategory.name=newName
        db.session.commit()
        return redirect(url_for('category.category_list'))
    return "Edit not found",404
@category_bp.route('/delete/<int:newCategory_id>',methods=['GET'])
def deleteNewCategory(newCategory_id):
    DeleteCategory=Category.query.get_or_404(newCategory_id)
    db.session.delete(DeleteCategory)
    db.session.commit()
    return redirect(url_for('category.category_list'))
 