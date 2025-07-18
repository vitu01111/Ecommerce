from flask import Flask,Blueprint,render_template,request,redirect
from src.Models.Product import Product
from src.Models.Order import Order
from src.Models.Category import Category
from src.Models.Admin import Admin
from src.db import db


dashborad_bp=Blueprint('dashborad',__name__)

@dashborad_bp.route('/',methods=['GET'])
def dashboard():
    ProductCount = db.session.query(Product).count()
    OrderCount = db.session.query(Order).count()
    CategoryCount = db.session.query(Category).count()
    AdminCount = db.session.query(Admin).count()
    return render_template('admin/dashborad.html',productCount = ProductCount,OrderCount=OrderCount,CategoryCount=CategoryCount,AdminCount=AdminCount)