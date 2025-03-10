from .extensions import db

from sqlalchemy.sql import func

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=False)
    retail_price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)  # tablets per strip, make a separate field later
    manufacturer = db.Column(db.String(200), nullable=True)
    supplier = db.Column(db.String(10), unique=False, nullable=True)
    batch_no = db.Column(db.String(10), unique=False, nullable=True)
    mfg_date = db.Column(db.DateTime, nullable=True, unique=False)
    exp_date = db.Column(db.DateTime, nullable=True, unique=False)
    unit_of_measure = db.Column(db.String(20), nullable=True, default='') # box, bottle, pouch, ...
    weight_per_unit = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True, onupdate=func.now())
    # One-to-Many relation with category
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    # Back reference to Category
    category = db.relationship('Category', back_populates='products')
    # One-to-Many relation with Inventory
    inventories = db.relationship('Inventory', back_populates='product')

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, retail_price={self.price}, manufacturer={self.manufacturer}, exp_date={self.exp_date})>"
    
    def get_list_view(self):
        return {
            'id': self.id,
            'name': self.name,
            'manufacturer': self.manufacturer,
            'batch_no': self.batch_no,
            'exp_date': self.exp_date
        }

    def get_detail_view(self):
        return {
            'id': self.id,
            'name': self.name,
            'retail_price': self.retail_price,
            'description': self.description,
            'manufacturer': self.manufacturer,
            'supplier': self.supplier,
            'batch_no': self.batch_no,
            'mfg_date': self.mfg_date,
            'exp_date': self.exp_date,
            'unit_of_measure': self.unit_of_measure,
            'weight_per_unit': self.weight_per_unit,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'category': {
                'id': self.category_id,
                'name': self.category.name
            }
        }
        
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(50), nullable=True, unique=False)
    products = db.relationship('Product', back_populates='category', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name})>"
    
    def get_list_view(self):
        return {"id": self.id, "name" : self.name}
    
    def get_detail_view(self):
        return {
            "id": self.id, "name": self.name, "description": self.description
        }

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    purchase_price = db.Column(db.Float, nullable=False)
    max_qty = db.Column(db.Float, nullable=False)
    available_qty = db.Column(db.Float, nullable=False)
    reorder_level = db.Column(db.Float, nullable=False)
    reorder_qty = db.Column(db.Float, nullable=False)
    shelf_no = db.Column(db.Integer, nullable=False)
    exp_date = db.Column(db.DateTime(timezone=True), nullable=True)
    is_available = db.Column(db.Boolean, default=False)
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now(), nullable=True)
    # Many-to-One relation with Product, one product can have multiple inventory records, absed on batch, warehouse, etc
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False) # DELETE logic?
    product = db.relationship("Product", back_populates="inventories")

    def __repr__(self):
        return f"<Inventory(id={self.id})>"
    
    def get_list_view(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "is_available": self.is_available,
            "shelf_no": self.shelf_no
        }
    
    def get_detail_view(self):
        return {
            "id": self.id,
            "product": {
                "id": self.product_id,
                "name": self.product.name,
                "retail_price": self.product.retail_price,
                "batch_no": self.product.batch_no
            },
            "purchase_price": self.purchase_price,
            "max_qty": self.max_qty,
            "available_qty": self.available_qty,
            "reorder_level": self.reorder_level,
            "reorder_qty": self.reorder_qty,
            "shelf_no": self.shelf_no,
            "exp_date": self.exp_date,
            "is_available": self.is_available,
            "updated_at": self.updated_at
        }
    