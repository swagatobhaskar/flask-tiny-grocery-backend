from .extensions import db
from sqlalchemy.sql import func

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=False)
    retail_price = db.Column(db.Float, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)  # tablets per strip, make a separate field later
    manufacturer = db.Column(db.String(200), nullable=True)
    exp_date = db.Column(db.DateTime, nullable=True, unique=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False, onupdate=func.now())
    unit_of_measure = db.Column(db.String(20), nullable=True, default='') # box, bottle, pouch, ...
    weight_per_unit = db.Column(db.Float, nullable=False)
    # Many-to-One relation with category
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    category = db.relationship('Category', back_populates='products')

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, retail_price={self.price}, manufacturer={self.manufacturer}, exp_date={self.exp_date})>"
    
    def list_view(self):
        return {
            'id': self.id,
            'name': self.name,
            'manufacturer': self.manufacturer,
            'exp_date': self.exp_date
        }

    def detail_view(self):
        return {
            'id': self.id,
            'name': self.name,
            'manufacturer': self.manufacturer,
            'retail_price': self.retail_price,
            'purchase_price': self.purchase_price,
            'exp_date': self.exp_date,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'unit_of_measure': self.unit_of_measure,
            'weight_per_unit': self.weight_per_unit,
        }
        
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(50), nullable=True, unique=False)
    products = db.relationship('Product', back_populates='category', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name})>"

class Inventory(db.Model):
    pass