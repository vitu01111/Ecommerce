from flask import Blueprint, render_template
from src.db import db
from src.Models.Employee import Employee

product_bp = Blueprint('product', __name__)

@product_bp.route('/', methods=['GET'])
def productIndex():
    queryEmployee = db.session.query(Employee).all()
    print(queryEmployee,"fjsfjslfjs")
    return render_template('web/product/index.html', employees=queryEmployee)

@product_bp.route('/detail', methods=['GET'])
def productDetail():
    return render_template('web/product/detail.html')