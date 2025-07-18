from src.db import db




class Products(db.Model):
    """
    Customer model for storing customer information
    Enhanced with validation, hooks, and utility methods
    """
    
    # Primary key
    id    = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name  = db.Column(db.String(100), nullable=False)