from app.extensions import db
from datetime import datetime


class Product (db.Model):
    __tablename__="products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    price_unit = db.Column(db.String(50),nullable=False ,default='UGX')
    quantity = db.Column(db.String(100),nullable=False)
    description = db.Column(db.String(255),nullable=False)
    created_at =db.Column(db.DateTime,default= datetime.now())
    updated_at =db.Column(db.DateTime,onupdate= datetime.now())
    


# product constructor
    def __init__(self,name,price_unit,quantity,description):
      self.name = name
      self.price_unit =price_unit
      self.quantity = quantity
      self.description = description


     # string representation
    def __repr__(self):
       return f"Product{self.name}" 
