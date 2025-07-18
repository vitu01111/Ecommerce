from flask import Blueprint,render_template,request,flash,redirect,url_for,session
from src.db import db 
from src.Models.TestLog import TestLog
from werkzeug.security import generate_password_hash,check_password_hash


testLog_bp=Blueprint('testLog',__name__)
@testLog_bp.route('login',methods=['GET'])
def testLog():
    return render_template('/web/TestLog/login.html')
@testLog_bp.route('loginGet',methods=['POST'])
def testLogData():
    username=request.form['username']
    passsword=request.form['password']
    user=TestLog.query.filter_by(username=username).first()
    if not username or not passsword:
        flash('Please enter both username and password','error')
    elif not user:
        flash('You do not have account.Please register.','error')
        return render_template('/web/TestLog/register.html')
    elif not check_password_hash(user.password,passsword):
         flash('Incorrect password.','error')
    else:
        session['user_id']=user.id
        flash('Login successful','success')
        return redirect(url_for(''))          