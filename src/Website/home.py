from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from src.Models.Admin import Admin
from src.db import db

home_bp = Blueprint('home', __name__, url_prefix='/')

@home_bp.route('/')
def index():
    admins = Admin.query.all()
    return render_template('web/index.html', admins=admins)

@home_bp.route('/detail', methods=['GET', 'POST'])
def detail():
    if request.method == 'POST':
        # Handle form submission
        pass
    return render_template('web/detail.html')

@home_bp.route('/ProcessCheckout')
def ProcessCheckout():
    admins = Admin.query.all()
    return render_template('web/processCheckout.html', admins=admins)


@home_bp.route('/Api/login', methods=['GET', 'POST'])
def api_login():
    if request.method == 'POST':
        try:
            request_data = request.get_json()
            ReqEmail = request_data.get('email', '')
            ReqPassword = request_data.get('password', '')
            if not ReqEmail or not ReqPassword:
                return {"message": "Email and password are required"}, 400
            # Validate the email and password
            admin = Admin.query.filter_by(email=ReqEmail).first()
            if admin and admin.check_password(ReqPassword):
                session['admin_id'] = admin.id  # Store admin ID in session
                session['unser_email'] = admin.email  # Store email in session
                session['name'] = admin.username  # Store username in session
                return {"message": "Login successful", "login": True}, 200
            return {"message": "Invalid email or password", "login": False}, 401
        except Exception as e:
            return {"message": f"Error processing request: {str(e)}", "login": False}, 500

# @home_bp.route('/login', methods=['GET', 'POST'])
# def login():
#     try:
#         form = LoginForm()
#         if form.validate_on_submit():
#             admin = Admin.query.filter_by(email=form.email.data).first()
#             if admin and admin.check_password(form.password.data):
#                 access_token = create_access_token(identity=admin.id)
#                 session['admin_id'] = admin.id 
#                 # You can return the token as JSON, set it as a cookie, or pass to the template
#                 flash('Login successful!', 'success')
#                 return redirect(url_for('customer_bp.customer_list'))
#                 # return render_template('admin/customers/index.html', form=form, access_token=access_token)
#             else:
#                 flash('Invalid email or password.', 'danger')
#         return render_template('auth/login.html', form=form)
#     except Exception as e:
#         flash(f'Error checking session: {str(e)}', 'danger')
#         return str(e)
    

