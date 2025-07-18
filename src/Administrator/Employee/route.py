from flask import Flask,Blueprint,render_template,request,redirect
from src.Administrator.Employee.form import EmployeeForm
from src.Models.Employee import Employee
from src.db import db


employee_bp=Blueprint('employee',__name__)

@employee_bp.route('/',methods=['GET'])
def employee_list():
    QueryEmployee = db.session.query(Employee).all()
    return render_template('admin/employee/index.html',data = QueryEmployee)

@employee_bp.route('/createForm',methods=['GET'])
def createEmployeeForm():
    form = EmployeeForm()
    return render_template('admin/employee/create.html',form=form)

@employee_bp.route('/insertEmployee',methods=['POST'])
def insertEmployee():
    reqName=request.form['name']
    itemEmployee = Employee(name=reqName)
    db.session.add(itemEmployee)
    db.session.commit()
    return redirect('/administrator/employee/')

@employee_bp.route('/editForm/<int:employee_id>',methods=['GET'])
def editEmployeeForm(employee_id):
    GetEmployee = db.session.query(Employee).filter_by(id=employee_id).first()
    form = EmployeeForm(obj=GetEmployee)
    return render_template('admin/employee/edit.html',form=form,GetEmployee=GetEmployee)

@employee_bp.route('/updateEmployee/<int:employee_id>',methods=['POST'])
def updateEmployee(employee_id):
    GetEmployee = db.session.query(Employee).filter_by(id=employee_id).first()
    if GetEmployee:
        newName = request.form['name']
        GetEmployee.name = newName
        db.session.commit()
        return redirect('/administrator/employee/')
    return "Edit not found", 404

@employee_bp.route('/delete/<int:id>',methods=['GET'])
def deleteEmployee(id):
    DeleteEmployee = db.session.query(Employee).filter_by(id=id).first()
    db.session.delete(DeleteEmployee)
    db.session.commit()
    return redirect('/administrator/employee/')