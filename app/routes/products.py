from flask import Blueprint, request, jsonify
from datetime import datetime

from ..extensions import db
from ..models import Product, Inventory, Category

product_bp = Blueprint(name='product', import_name='__name__')

@product_bp.route('/')
def home():
    return jsonify({'messgae': 'Hello, World! This is the Product Route.'}), 200

@product_bp.route('/list-view', methods=["GET"])
def get_product_list():
    all_products = Product.query.all()
    return jsonify([product.list_view() for product in all_products]), 200

@product_bp.route('/detail-view/<int:id>', methods=["GET"])
def get_product_detail(id):
    selected_product = Product.query.filter_by(id=id).first()
    if not selected_product:
            return jsonify({'error': f"Product with id {id} not found"}), 404
    return jsonify(selected_product.detail_view()), 200

@product_bp.route('/add-new', methods=["POST"])
def create_product():
    if request.method == "POST":
        data = request.get_json()

        required_batch = Batch.query.get(data['batch_id'])
        if not required_batch:
            return jsonify({'error': f"Batch with id {id} not found"}), 404
        required_batch = Batch.query.get(data['batch_id'])
        if not required_batch:
            return jsonify({'error': f"Batch with id {id} not found"}), 404
        
        new_product = Product(
            name = data['name'],
            manufacturer = data['manufacturer'],
            price = data['price'],
            exp_date = datetime.fromisoformat(data['exp_date']),
            weight = data['weight'],
            unit_of_measure = data['unit_of_measure'],
            supplier = data['supplier'],
            batch = required_batch
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
        if 'manufacturer' in data:
            fetched_product.manufacturer = data['manufacturer']
        if 'unit_price' in data:
            fetched_product.unit_price = data['unit_price']
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
        if 'weight' in data:
            fetched_product.weight = data['weight']
        if 'unit_of_measure' in data:
            fetched_product.unit_of_measure = data['unit_of_measure']
        if 'supplier' in data:
            fetched_product.supplier = data['supplier']
        if 'category_id' in data:
            category_to_assign = Category.query.get(data['category_id'])
            if not category_to_assign:
                return jsonify({'error': 'Category not found'}), 404
            fetched_product.category = category_to_assign
        if 'subcategory_id' in data:
            subcategory_to_assign = Subcategory.query.get(data['subcategory_id'])
            if not subcategory_to_assign:
                return jsonify({'error': 'Subcategory not found'}), 404
            fetched_product.subcategory = subcategory_to_assign

        db.session.commit()
        return jsonify({'message': 'Product updated successfully!'}), 200


@product_bp.route('/delete-product/<int:id>', methods=["DELETE"])
def delete_product_by_id(id):
    if request.method == 'DELETE':
        selected_product = db.session.get(Product, id)
        if not selected_product:
            return jsonify({'error': f"Product with id {id} not found"}), 404
        
        db.session.delete(selected_product)
        db.session.commit()

        return jsonify({'message': 'Product deleted successfully!'}), 200
