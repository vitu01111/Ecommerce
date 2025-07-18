
from src.db import db
from flask import Blueprint,flash,render_template,request,session,url_for,redirect
from src.Models.User import User

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

login_bp=Blueprint('login',__name__)  



def set_password(password):
    password = bcrypt.generate_password_hash(password).decode('utf-8')

def check_password(db_password, enter_password):
    return bcrypt.check_password_hash(db_password,enter_password)

@login_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pass
    return render_template('web/auth/login.html')

@login_bp.route('/Api', methods=['GET', 'POST'])
def api_login():
    if request.method == 'POST':
        try:
            request_data = request.get_json()
            ReqEmail = request_data.get('email', '')
            ReqPassword = request_data.get('password', '')
            if not ReqEmail or not ReqPassword:
                return {"message": "Email and password are required"}, 400
            # Validate the email and password
            # user = User.query.filter_by(email=ReqEmail).first()
            user = db.session.query(User).filter_by(email=ReqEmail).first()
            if user and check_password(user.password,ReqPassword):
                session['user_id'] = user.id  # Store admin ID in session
                session['user_email'] = user.email  # Store email in session
                session['name'] = user.username  # Store username in session
                return {
                        "message": "Login successful", 
                        "login": True
                    }, 200
            
            return {
                    "message": "Invalid email or password", 
                    "login": False
                }, 401
        except Exception as e:
            return {
                "message": f"Error processing request: {str(e)}", "login": False}, 500
    
@login_bp.route('/logout',methods=['GET'])
def logout():
    session.clear()  # Remove all session data
    return redirect(url_for('product_bp.index'))

@login_bp.route('/register',methods=['GET','POST'])
def register():
    return render_template('web/auth/register.html')