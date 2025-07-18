from src.db import db
from flask import Blueprint, flash, render_template, request, redirect, url_for
from src.Models.User import User
from flask_bcrypt import Bcrypt

register_bp = Blueprint('register', __name__)
bcrypt = Bcrypt()

@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
 
        password = request.form['password']
        if not username or not email or not password:
            flash('Please complete all fields', 'error')
        elif User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
        elif User.query.filter_by(email=email).first():
            flash('Email already registered', 'error') 

        else:
            
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                new_user = User(username=username, email=email, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('login.login'))

    return render_template('web/auth/register.html', form_action='')
