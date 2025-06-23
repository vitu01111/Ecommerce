from src.db import db

class Employee(db.Model):
    
    # Primary key
    id    = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name  = db.Column(db.String(100), nullable=False)
    