# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Main Flask Application for Ecommerce Project
Integrates all components    app.run(debug=True, host='0.0.0.0', port=5005)and provides a complete working application
"""

from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, session
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
# from src.Website.product.route import product_bp  


# Import our database utilities
from src.db import init_db, create_tables, DatabaseConfig

# Load environment variables
load_dotenv()

# app = Flask(__name__)
app = Flask(__name__, 
           template_folder='templates',
           static_folder='.',
           static_url_path='')

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'super-secret-jwt-key')

# Initialize database using our db utilities
db = init_db(app)
jwt = JWTManager(app)

# Website
# Import and register blueprints
from src.Website.home import home_bp
# from src.Website.product.route import product_bp

#for product login
from src.Website.products.route import product_bp
from src.Website.productsOld.route import productOld_bp
from src.Website.loginProduct.route import loinProduct_bp
# from src.Website.TestLog.rounte import testLog_bp
from src.Website.Image.route import image_bp
from src.Website.Order.route import order_router
from src.Website.auth.login import login_bp
from src.Website.auth.register import register_bp

app.register_blueprint(home_bp, url_prefix='/dd')
app.register_blueprint(product_bp,url_prefix='/')

app.register_blueprint(productOld_bp,url_prefix='/website/products')
app.register_blueprint(loinProduct_bp,url_prefix='/website/loginProduct')
app.register_blueprint(image_bp,url_prefix='/image/image')
app.register_blueprint(order_router,url_prefix='/order')
app.register_blueprint(login_bp, url_prefix='/website/login')
app.register_blueprint(register_bp, url_prefix='/website/register')


# Admin
# Import and register blueprints
from src.Administrator.Customer.route import customer_bp
from src.Administrator.ClassRoom.route import classroom_bp
from src.Administrator.Order.route import order_bpp
 

from src.Administrator.Admin.route import admin_bp
from src.Administrator.Auth.route import auth_bp
from src.Administrator.Product.route import prdouct_bp
from src.Administrator.Category.route import category_bp
from src.Administrator.Employee.route import employee_bp
from src.Administrator.Slider.Slider import slider_bp
from src.Administrator.dashboard.route import dashborad_bp


app.register_blueprint(dashborad_bp,url_prefix='/administrator/dashboard')

app.register_blueprint(slider_bp,url_prefix='/administrator/slider')
app.register_blueprint(customer_bp, url_prefix='/administrator/customers')
app.register_blueprint(classroom_bp, url_prefix='/administrator/classrooms')
app.register_blueprint(order_bpp, url_prefix='/administrator/orders')
app.register_blueprint(admin_bp, url_prefix='/administrator/admins')
app.register_blueprint(auth_bp, url_prefix='/auth')

app.register_blueprint(prdouct_bp, url_prefix='/administrator/product')
app.register_blueprint(category_bp,url_prefix='/administrator/category')

app.register_blueprint(employee_bp,url_prefix='/administrator/employee')

# API
# Import and register blueprints
from src.Api.order import order_api

app.register_blueprint(order_api,url_prefix='/api/order')

@app.before_request
def make_session_permanent():
    session.permanent = True

if __name__ == '__main__':
    # app = create_app()
    # print("🚀 Starting Flask Ecommerce Application")
    print("📍 Available routes:")
    print("   - http://localhost:5002")
    
    app.run(debug=True, host='0.0.0.0', port=5002)
