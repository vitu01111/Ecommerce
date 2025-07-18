from src.db import db
from src.Models.User import User
from flask import Blueprint,flash,render_template,request,redirect,url_for,session
from werkzeug.security import generate_password_hash, check_password_hash
loinProduct_bp=Blueprint('loginPro',__name__)       


@loinProduct_bp.route('/login', methods=['GET'])
def loginProduct():
    return render_template('web/loginProduct/loginProduct.html')

@loinProduct_bp.route('/loginsubmit', methods=['POST'])
def loginProductData():
    username = request.form['username']
    password = request.form['password']
    
    #we use this for get to use for search name when we need to search by username
    user = User.query.filter_by(username=username).first()

    #if we don't have username or password then we will show this message    
    if not username or not password:
        flash('Please enter both username and password', 'error')

    # if for check if we have already username and password if we don't have so it will to register   
    elif not user:
        flash('You do not have account. Please register.', 'error')
        return redirect(url_for('loginPro.registerProduct'))
    
    #if we have username but password is not correct then it will show this message
    elif not check_password_hash(user.password, password):
        flash('Incorrect password.', 'error')

    #if we have username and password is correct then it will login
    else:
        session['user_id'] = user.id
        flash('Login successful', 'success')
        return redirect(url_for('productOld_bp.index'))
    return render_template('web/loginProduct/loginProduct.html')

@loinProduct_bp.route('/register', methods=['GET'])
def registerProduct():
    return render_template('web/loginProduct/register.html')

@loinProduct_bp.route('/registersubmit', methods=['POST'])
def registerProductData():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    password = request.form['password']
    email = request.form['email']
    if not username or not password or not email:
        flash('Please fill in all fields', 'error')
    elif User.query.filter_by(username=username).first():
        flash('Username already exists', 'error')
    elif User.query.filter_by(email=email).first():
        flash('Email already exists', 'error')
    else:
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, email=email)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('loginPro.loginProduct'))
    return render_template('web/loginProduct/register.html')
 

@loinProduct_bp.route('/logoutPro')
def logoutProduct():
    session.clear()
    flash('You have been logged out','success')
    return redirect(url_for('productOld_bp.index'))


