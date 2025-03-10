from flask import Blueprint, request, jsonify
from datetime import datetime

from ..extensions import db
from ..models import Product, Category

product_bp = Blueprint(name='product', import_name='__name__')

@product_bp.route('/')
def home():
    return jsonify({'messgae': 'Hello, World! This is the Product Route.'}), 200

@product_bp.route('/list-view', methods=["GET"])
def get_product_list():
    all_products = Product.query.all()
    return jsonify([product.get_list_view() for product in all_products]), 200

@product_bp.route('/detail-view/<int:id>', methods=["GET"])
def get_product_detail(id):
    selected_product = Product.query.filter_by(id=id).first()
    if not selected_product:
            return jsonify({'error': f"Product with id {id} not found"}), 404
    return jsonify(selected_product.get_detail_view()), 200

@product_bp.route('/add-new', methods=["POST"])
def create_product():
    if request.method == "POST":
        data = request.get_json()

        required_category = Category.query.get(data['category_id'])
        if not required_category:
            return jsonify({'error': f"category with id {id} not found"}), 404
        required_category = Category.query.get(data['category_id'])
        if not required_category:
            return jsonify({'error': f"category with id {id} not found"}), 404
        
        new_product = Product(
            name = data['name'],
            retail_price = data['retail_price'],
            description = data['description'],
            manufacturer = data['manufacturer'],
            supplier = data['supplier'],
            batch_no = data['batch_no'],
            mfg_date = datetime.fromisoformat(data['mfg_date']),
            exp_date = datetime.fromisoformat(data['exp_date']),
            unit_of_measure = data['unit_of_measure'],
            weight_per_unit = data['weight_per_unit'],
            category = required_category
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"message": "Product added successfully!"}), 201


@product_bp.route('/edit/<int:id>', methods=["PUT"])
def edit_category(id):
    if request.method == 'PUT':
        fetched_product = db.session.get(Product, id)
        if not fetched_product:
            return jsonify({'error': f"Product with id {id} not found"}), 404
        
        data = request.get_json()
        # print("DATA::", data)
        if not data:
            return jsonify({"error": "Invalid data!"}), 400

        # Update fields only if they are present in the request body
        if 'name' in data:
            fetched_product.name = data['name']
        if 'retail_price' in data:
            fetched_product.retail_price = data['retail_price']
        if 'description' in data:
            fetched_product.description = data['description']
        if 'mfg_date' in data:
            try:
                fetched_product.mfg_date = datetime.fromisoformat(data['mfg_date'])
            except ValueError:
                return jsonify({"error": "Invalid manufacturing date format. Use ISO 8601 format (YYYY-MM-DDTHH:MM:SS)"}), 400
        if 'batch_no' in data:
            fetched_product.batch_no = data['batch_no']
        if 'exp_date' in data:
            try:
                fetched_product.exp_date = datetime.fromisoformat(data['exp_date'])
            except ValueError:
                return jsonify({"error": "Invalid expiration date format. Use ISO 8601 format (YYYY-MM-DDTHH:MM:SS)"}), 400
        if 'weight_per_unit' in data:
            fetched_product.weight_per_unit = data['weight_per_unit']
        if 'unit_of_measure' in data:
            fetched_product.unit_of_measure = data['unit_of_measure']
        if 'manufacturer' in data:
            fetched_product.manufacturer = data['manufacturer']
        if 'supplier' in data:
            fetched_product.supplier = data['supplier']
        if 'category_id' in data:
            category_to_assign = Category.query.get(data['category_id'])
            if not category_to_assign:
                return jsonify({'error': 'Category not found'}), 404
            fetched_product.category = category_to_assign
       
        db.session.commit()
        return jsonify({'message': 'Product updated successfully!'}), 200


@product_bp.route('/delete/<int:id>', methods=["DELETE"])
def delete_product_by_id(id):
    if request.method == 'DELETE':
        selected_product = db.session.get(Product, id)
        if not selected_product:
            return jsonify({'error': f"Product with id {id} not found"}), 404
        
        db.session.delete(selected_product)
        db.session.commit()

        return jsonify({'message': 'Product deleted successfully!'}), 200
